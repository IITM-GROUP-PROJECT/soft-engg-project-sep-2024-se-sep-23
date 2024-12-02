<template>
  <div class="project-info">
    <nav class="navbar">
        <div class="navbar-content">
            <div class="navbar-left">
                <button @click="goBack" class="back-btn">
                <i class="fas fa-arrow-left"></i>
                Back
                </button>
                <div class="navbar-brand">
                <img src="/iitm.png" alt="IITM Logo" class="navbar-logo" />
                <span>Project Information</span>
                </div>
            </div>
            <button @click="logout" class="logout-btn">
                <i class="fas fa-sign-out-alt"></i>
                Logout
            </button>
            </div>
    </nav>

    <div class="container">
      <div class="project-header">
        <h2>{{ project.title }}</h2>
        <div class="course-badge">{{ project.course }}</div>
        <div class="project-description">{{ project.problem }}</div>
      </div>

      <div class="content-grid">
        <div class="main-content">
          <div class="section-header">
            <h3><i class="fas fa-tasks"></i> Milestones</h3>
          </div>
          <div class="milestones-container">
            <div v-for="milestone in project.milestones" 
                 :key="milestone.id" 
                 class="milestone-card"
                 :class="{ 'completed': milestone.status === 'Completed' }">
              <div class="milestone-status">
                <span :class="['status-badge', milestone.status.toLowerCase()]">
                  {{ milestone.status }}
                </span>
              </div>
              <div class="milestone-content">
                <p class="milestone-description">{{ milestone.title }}</p>
                <p class="milestone-description">{{ milestone.description }}</p>
                <p class="milestone-deadline">
                  <i class="far fa-calendar-alt"></i>
                  Due: {{ milestone.deadline }}
                </p>
              </div>
              <button v-if="milestone.status === 'Pending'" 
                      @click="markAsCompleted(milestone.id)" 
                      class="complete-btn">
                <i class="fas fa-check"></i>
                Mark Complete
              </button>
            </div>
          </div>
        </div>

        <div class="side-content">
          <div class="project-form">
            <div class="section-header">
              <h3><i class="fab fa-github"></i> Project Resources</h3>
            </div>
            
            <div class="form-group">
                <label for="github_repo_url">GitHub Repository URL</label>
                <div class="input-group">
                    <i class="fab fa-github"></i>
                    <a 
                    :href="project.github_repo_url"
                    class="repo-link"
                    target="_blank"
                    rel="noopener noreferrer"
                    >
                    {{ project.github_repo_url }}
                    </a>
                </div>
            </div>

            <div class="form-group">
              <label for="project_report">Upload Project Report (PDF)</label>
              <input 
                type="file"
                id="project_report"
                @change="handleFileUpload"
                class="form-control" 
                accept="application/pdf"
              />
              <div class="mt-3">
                <div v-if="downloadError" class="error-message">
                  {{ downloadError }}
                </div>
                <button v-if="project.project_report" @click="downloadPdf" class="btn btn-brown">
                  <i class="fas fa-download"></i> Download Existing Report
                </button>
                <div v-else class="text-muted">
                  You have not submitted a report yet.
                </div>
              </div>
            </div>

            <button @click="saveChanges" class="save-btn">
              <i class="fas fa-save"></i>
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'ProjectInfo',
  data() {
    return {
      downloadError: null,
      project: {
        title: '',
        problem: '',
        course: '',
        milestones: [],
        github_repo_url: '',
        project_report: null,
      }
    };
  },
  methods: {
    async fetchProjectInfo() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/project_info/${this.$route.params.id}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log(data);
        this.project = data;
      } catch (error) {
        console.error('Error fetching project info:', error);
      }
    },
    markAsCompleted(milestoneId) {
      const milestone = this.project.milestones.find(m => m.id === milestoneId);
      if (milestone) {
        milestone.status = 'Completed';
      }
    },
    handleFileUpload(event) {
      this.project.project_report_pdf = event.target.files[0];  
    },
    async downloadPdf() {
      this.downloadError = null;
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/project_info/student/project_report/${this.$route.params.id}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });

        if (response.status === 404) {
          this.downloadError = "Report not submitted";
          return;
        }

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "ProjectReport.pdf");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error("Error downloading the file:", error);
        this.downloadError = "Error downloading the file";
      }
    },
    async saveChanges() {
      try {
        const projectId = this.$route.params.id;
        const formData = new FormData();
        formData.append('project_report', this.project.project_report_pdf); 
        formData.append('data', JSON.stringify(this.project)); 

        const response = await fetch(`http://127.0.0.1:5000/api/project_info/${projectId}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: formData
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        window.location.reload();
        alert('Project info saved successfully!');
      } catch (error) {
        console.error('Error saving project info:', error);
      }
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
    },
    goBack() {
      this.$router.push('/student_dashboard');
    }
  },
  created() {
    this.fetchProjectInfo();
  }
};
</script>


<style scoped>
.project-info {
  min-height: 100vh;
  background-color: #f8f9fa;
  padding-top: 9rem;
}

.navbar {
  background-color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 0.75rem 1.5rem;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.navbar-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #791912;
  font-size: 1.25rem;
  font-weight: 600;
}

.navbar-logo {
  height: 40px;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 6px;
  color: #791912;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background-color: #791912;
  color: white;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 6px;
  color: #791912;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background-color: #791912;
  color: white;
}

.container {
  max-width: 1200px;
  margin: 0 auto; /* Changed from 'auto 2rem' to '0 auto' for proper centering */
  padding: 0 1.5rem;
  width: 90%; /* Added to ensure consistent width */
}

.project-header {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.project-header h2 {
  color: #791912;
  margin-bottom: 1rem;
}

.project-description {
  color: #666;
  line-height: 1.6;
}

.course-badge {
  display: inline-block;
  background-color: #f0f0f0;
  color: #666;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  margin: 0.5rem 0 1rem 0;
}

.content-grid {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 2rem;
}

.section-header {
  margin-bottom: 1.5rem;
}

.section-header h3 {
  color: #791912;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.milestone-card {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}

.milestone-card:hover {
  transform: translateY(-2px);
}

.milestone-card.completed {
  border-left: 4px solid #28a745;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-badge.pending {
  background-color: #fff3cd;
  color: #856404;
}

.status-badge.completed {
  background-color: #d4edda;
  color: #155724;
}

.milestone-content {
  margin: 1rem 0;
}

.milestone-description {
  color: #444;
  margin-bottom: 0.5rem;
}

.milestone-deadline {
  color: #666;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.complete-btn {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background-color 0.3s ease;
}

.complete-btn:hover {
  background-color: #218838;
}

.repo-link {
  color: #0366d6;
  text-decoration: none;
  padding: 0.75rem 2.5rem;
  display: block;
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 6px;
  word-break: break-all;
}

.repo-link:hover {
  text-decoration: underline;
  color: #0366d6;
}

.project-form {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #444;
  font-weight: 500;
}

.input-group {
  position: relative;
}

.input-group i {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  transition: border-color 0.3s ease;
}

.input-group .form-control {
  padding-left: 2.5rem;
}

.form-control:focus {
  outline: none;
  border-color: #791912;
}

textarea.form-control {
  resize: vertical;
  min-height: 120px;
}

.error-message {
  color: #dc3545;
  margin: 10px 0;
  padding: 8px;
  background-color: #fff5f5;
  border-radius: 4px;
  font-size: 0.9rem;
}

.btn-brown {
  background-color: #791912;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-brown:hover {
  background-color: #5d130e;
}

.text-muted {
  color: #6c757d;
  margin-top: 8px;
}

.mt-3 {
  margin-top: 1rem;
}

.save-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #d7a84e;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: background-color 0.3s ease;
}

.save-btn:hover {
  background-color: #c29843;
}

/* Adjust for larger screens */
@media (min-width: 1200px) {
  .content-grid {
    /* Increase the width of both columns on large screens */
    grid-template-columns: 3fr 1.5fr;
  }
}

@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .navbar-content {
    flex-direction: column;
    gap: 1rem;
  }
  
  .container {
    margin-top: 8rem;
  }
}
</style>
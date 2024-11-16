<template>
  <div class="project-details">
    <nav class="navbar">
      <div class="navbar-content">
        <div class="navbar-brand">
          <img src="/iitm.png" alt="IITM Logo" class="navbar-logo" />
          <span>Project Overview</span>
        </div>
        <div class="nav-actions">
          <button @click="goBack" class="back-btn">
            <i class="fas fa-arrow-left"></i>
            Back to Dashboard
          </button>
          <button @click="logout" class="logout-btn">
            <i class="fas fa-sign-out-alt"></i>
            Logout
          </button>
        </div>
      </div>
    </nav>

    <div class="container">
      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <i class="fas fa-spinner fa-spin"></i>
        <p>Loading project details...</p>
      </div>

      <div v-else class="content">
        <!-- Project Info Card -->
        <!-- Update the Project Info Card section -->
          <div class="section-card project-info-card">
            <div class="card-header">
              <div class="title-section">
                <h2>{{ project.title }}</h2>
                <div class="course-badge">{{ project.course }}</div>
              </div>
              <div class="action-buttons">
                <button @click="editProject" class="edit-btn">
                  <i class="fas fa-edit"></i>
                  Edit Project
                </button>
                <button @click="deleteProject" class="delete-btn">
                  <i class="fas fa-trash"></i>
                  Delete
                </button>
              </div>
            </div>
            <div class="problem-statement">
              <h3>Problem Statement</h3>
              <p>{{ project.problem }}</p>
            </div>
          </div>

        <!-- Milestones Section -->
        <div class="section-card">
          <h3><i class="fas fa-tasks"></i> Project Milestones</h3>
          <div class="milestones-list">
            <div v-for="(milestone, index) in project.milestones" :key="milestone.id || index" class="milestone-card">
              <div class="milestone-number">#{{ index + 1 }}</div>
              <div class="milestone-content">
                <p class="milestone-text">{{ milestone.title }}</p>
                <p class="milestone-text">{{ milestone.description }}</p>
                <p class="milestone-deadline">
                  <i class="far fa-calendar-alt"></i>
                  Due: {{ new Date(milestone.deadline).toLocaleDateString() }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Students Section -->
        <div class="section-card">
          <h3><i class="fas fa-users"></i> Assigned Students</h3>
          <div class="search-container">
            <input type="text" class="search-bar" placeholder="Search Students..." v-model="searchQuery">
            <i class="fas fa-search search-icon"></i>
          </div>

          <div class="students-grid">
            <div v-for="student in project.students" :key="student.id" class="student-card">
              <div class="student-info">
                <i class="fas fa-user-graduate"></i>
                <span>{{ student.email }}</span>
              </div>
              <button @click="trackProgress(student.id)" class="track-btn">
                <i class="fas fa-chart-line"></i>
                Track Progress
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'ProjectDetails',
  data() {
    return {
      project: {
        title: '',
        problem: '',
        milestones: [],
        students: []
      },
      loading: true
    };
  },
  methods: {
    goBack() {
      this.$router.push('/instructor_dashboard');
    },
    async fetchProjectDetails() {
      this.loading = true;
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/project_details/${this.$route.params.projectId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        this.project = data;
      } catch (error) {
        console.error('Error fetching project details:', error);
      } finally {
        this.loading = false;
      }
    },
    editProject() {
      this.$router.push(`/edit_project/${this.$route.params.projectId}`);
    },
    async deleteProject() {
      if (confirm('Are you sure you want to delete this project?')) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/api/delete_project/${this.$route.params.projectId}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const data = await response.json();
          alert(data.msg);
          this.$router.push('/instructor_dashboard');
        } catch (error) {
          console.error('Error deleting project:', error);
        }
      }
    },
    trackProgress(studentId) {
      this.$router.push(`/track_progress/${this.$route.params.projectId}/${studentId}`);
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
    }
  },
  created() {
    this.fetchProjectDetails();
  }
};
</script>

<style scoped>
/* Add these styles in the <style scoped> section */

.search-container {
  position: relative;
  width: 100%;
  max-width: 400px;
  margin: 1rem 0;
}

.search-bar {
  width: 100%;
  padding: 12px 45px 12px 20px;
  border: 2px solid #e0e0e0;
  border-radius: 25px;
  font-size: 14px;
  background-color: white;
  transition: all 0.3s ease;
}

.search-bar:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 5px rgba(74, 144, 226, 0.3);
}

.search-bar:hover {
  border-color: #bdbdbd;
}

.search-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #757575;
  font-size: 18px;
}

/* Responsive styles */
@media (max-width: 768px) {
  .search-container {
    max-width: 100%;
  }

  .search-bar {
    padding: 10px 40px 10px 15px;
    font-size: 13px;
  }
}


.project-details {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.navbar {
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0.75rem 1.5rem;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.navbar-content {
  max-width: 1400px;
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

.nav-actions {
  display: flex;
  gap: 1rem;
}

.back-btn,
.logout-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn {
  background-color: transparent;
  border: 1px solid #791912;
  color: #791912;
}

.back-btn:hover {
  background-color: #791912;
  color: white;
}

.logout-btn {
  background-color: #dc3545;
  border: none;
  color: white;
}

.logout-btn:hover {
  background-color: #c82333;
}

.container {
  max-width: 1400px;
  margin: 6rem auto 2rem;
  padding: 0 2rem;
}

.section-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.project-info-card {
  border-top: 4px solid #791912;
}

.title-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.course-badge {
  display: inline-block;
  background-color: #f0f0f0;
  color: #666;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.card-header h2 {
  color: #791912;
  margin: 0;
}

.action-buttons {
  display: flex;
  gap: 1rem;
}

.edit-btn,
.delete-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-btn {
  background-color: #d7a84e;
  border: none;
  color: white;
}

.edit-btn:hover {
  background-color: #c29843;
}

.delete-btn {
  background-color: transparent;
  border: 1px solid #dc3545;
  color: #dc3545;
}

.delete-btn:hover {
  background-color: #dc3545;
  color: white;
}

.problem-statement h3 {
  color: #666;
  margin-bottom: 0.5rem;
}

.problem-statement p {
  color: #444;
  line-height: 1.6;
}

.milestones-list {
  display: grid;
  gap: 1rem;
}

.milestone-card {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 8px;
  align-items: center;
}

.milestone-number {
  background-color: #f8f9fa;
  color: #791912;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: 600;
}

.milestone-content {
  flex: 1;
}

.milestone-text {
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

.students-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 1.5rem;
}

.student-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  border: 1px solid #eee;
  border-radius: 8px;
  transition: all 0.3s ease;
  min-width: 0;
}

.student-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #444;
  min-width: 0;
  flex: 1;
}

.student-info span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.student-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #444;
}

.track-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background-color: #791912;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  margin-left: 1.5rem;
  flex-shrink: 0;
  min-width: 150px;
}

.track-btn:hover {
  background-color: #8a1c14;
}

.loading-state {
  text-align: center;
  padding: 3rem;
}

.loading-state i {
  color: #d7a84e;
  font-size: 2rem;
  margin-bottom: 1rem;
}

@media (max-width: 992px) {
  .card-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .action-buttons {
    width: 100%;
    justify-content: stretch;
  }
  .students-grid {
    grid-template-columns: 1fr;
  }

  .student-card {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
    text-align: center;
  }

  .student-info {
    justify-content: center;
  }

  .track-btn {
    width: 100%;
    justify-content: center;
    margin-left: 0;
  }
}
</style>
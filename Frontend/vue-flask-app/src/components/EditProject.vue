<template>
  <div class="edit-project">
    <nav class="navbar">
      <div class="navbar-content">
        <div class="navbar-brand">
          <img src="/iitm.png" alt="IITM Logo" class="navbar-logo" />
          <span>Edit Project</span>
        </div>
        <button @click="goBack" class="back-btn">
          <i class="fas fa-arrow-left"></i>
          Back
        </button>
      </div>
    </nav>

    <div class="container">
      <div v-if="loading" class="loading-state">
        <i class="fas fa-spinner fa-spin"></i>
        <p>Loading project...</p>
      </div>

      <div v-else class="form-card">
        <form @submit.prevent="updateProject">
          <div class="form-section">
            <h3>Project Details</h3>
            <div class="form-group">
              <label>Project Title</label>
              <input type="text" v-model="project.title" required>
            </div>
            <div class="form-group">
              <label>Problem Statement</label>
              <textarea v-model="project.problem" rows="4" required></textarea>
            </div>
          </div>

          <div class="form-section">
            <div class="milestone-header">
              <h3>Project Milestones</h3>
              <button type="button" @click="addMilestone" class="add-milestone-btn">
                <i class="fas fa-plus"></i> Add Milestone
              </button>
            </div>
            <div class="milestones-container">
              <div v-for="(milestone, index) in project.milestones" 
                   :key="milestone.id || index" 
                   class="milestone-card">
                <div class="milestone-number">#{{ index + 1 }}</div>
                <div class="milestone-inputs">
                  <input 
                    type="text" 
                    v-model="milestone.text"
                    placeholder="Milestone Description"
                    required
                  >
                  <input 
                    type="date" 
                    v-model="milestone.deadline"
                    required
                  >
                </div>
                <button 
                  type="button"
                  @click="removeMilestone(index)" 
                  class="remove-btn"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="submit-btn">
              <i class="fas fa-save"></i> Save Changes
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'EditProject',
  data() {
    return {
      project: {
        title: '',
        problem: '',
        milestones: []
      },
      loading: true
    }
  },
  methods: {
    goBack() {
      this.$router.push(`/project/${this.$route.params.projectId}`);
    },
    async fetchProjectDetails() {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/project_details/${this.$route.params.projectId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (!response.ok) throw new Error('Failed to fetch project');
      const data = await response.json();
      this.project = {
        ...data,
        milestones: data.milestones.map(m => ({
          ...m,
          deadline: new Date(m.deadline).toISOString().split('T')[0] // Convert to YYYY-MM-DD
        }))
      };
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to load project details');
    } finally {
      this.loading = false;
    }
    },
    addMilestone() {
    this.project.milestones.push({
      text: '',
      deadline: new Date().toISOString().split('T')[0] // Today's date in YYYY-MM-DD
    });
  },
    removeMilestone(index) {
      this.project.milestones.splice(index, 1);
    },
    async updateProject() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/update_project/${this.$route.params.projectId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(this.project)
        });
        
        if (!response.ok) throw new Error('Failed to update project');
        
        alert('Project updated successfully');
        this.$router.push(`/project/${this.$route.params.projectId}`);
      } catch (error) {
        console.error('Error:', error);
        alert('Failed to update project');
      }
    }
  },
  created() {
    this.fetchProjectDetails();
  }
}
</script>


<style scoped>
.edit-project {
  min-height: 100vh;
  background-color: #f8f9fa;
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

.container {
  max-width: 1600px;
  margin: 6rem auto 2rem;
  padding: 0 1.5rem;
}

.form-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.form-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #eee;
}

.form-section h3 {
  color: #791912;
  margin-bottom: 1.5rem;
  font-size: 1.25rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #444;
  font-weight: 500;
}

input, textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #eee;
  border-radius: 6px;
  transition: all 0.3s ease;
}

input:focus, textarea:focus {
  outline: none;
  border-color: #791912;
}

.milestone-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.milestone-card {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 1rem;
  align-items: center;
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.milestone-number {
  color: #791912;
  font-weight: 600;
}

.milestone-inputs {
  display: grid;
  gap: 0.5rem;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  background: transparent;
  border: 1px solid #791912;
  color: #791912;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: #791912;
  color: white;
}

.add-milestone-btn {
  background: #d7a84e;
  border: none;
  color: white;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: 6px;
  cursor: pointer;
}

.add-milestone-btn:hover {
  background: #c29843;
}

.remove-btn {
  background: transparent;
  border: none;
  color: #dc3545;
  padding: 0.5rem;
  cursor: pointer;
}

.remove-btn:hover {
  color: #bd2130;
}

.submit-btn {
  width: 100%;
  background: #791912;
  border: none;
  color: white;
  font-weight: 500;
  padding: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
}

.submit-btn:hover {
  background: #8a1c14;
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
  
  .form-card {
    padding: 1.5rem;
  }
  
  .milestone-card {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .milestone-number {
    margin-bottom: 0.5rem;
  }
}
</style>
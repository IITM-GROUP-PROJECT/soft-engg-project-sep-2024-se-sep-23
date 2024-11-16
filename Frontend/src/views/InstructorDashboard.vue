<template>
  <div class="instructor-dashboard">
    <nav class="navbar">
      <div class="navbar-content">
        <div class="navbar-brand">
          <img src="/iitm.png" alt="IITM Logo" class="navbar-logo" />
          <span>Instructor Dashboard</span>
        </div>
        <button @click="logout" class="logout-btn">
          <i class="fas fa-sign-out-alt"></i>
          Logout
        </button>
      </div>
    </nav>

    <div class="dashboard-container">
      <div class="dashboard-header">
        <h2>My Projects</h2>
        <button @click="createProject" class="create-btn">
          <i class="fas fa-plus"></i>
          Create New Project
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <i class="fas fa-spinner fa-spin"></i>
        <p>Loading projects...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="projects.length === 0" class="empty-state">
        <i class="fas fa-folder-open"></i>
        <p>No projects created yet</p>
        <button @click="createProject" class="create-btn">
          Create Your First Project
        </button>
      </div>

      <!-- Projects Grid -->
      <div v-else class="projects-grid">
        <div v-for="project in projects" :key="project.id" class="project-card">
          <div class="project-card-content">
            <h3>{{ project.title }}</h3>
            <div class="course-badge">{{ project.course }}</div>
            <p class="project-stats">
              <span><i class="fas fa-users"></i> {{ project.student_count || 0 }} Students</span>
              <span><i class="fas fa-tasks"></i> {{ project.milestone_count || 0 }} Milestones</span>
            </p>
            <button @click="viewDetails(project.id)" class="view-btn">
              <i class="fas fa-eye"></i>
              View Details
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'InstructorDashboard',
  data() {
    return {
      projects: [], 
      loading: true
    };
  },
  methods: {
    async fetchProjects() {
      this.loading = true;
      try {
        const response = await fetch('http://127.0.0.1:5000/api/instructor_dashboard', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.projects = await response.json();
      } catch (error) {
        console.error('Error fetching projects:', error);
      } finally {
        this.loading = false;
      }
    },
    viewDetails(projectId) {
      this.$router.push(`/project/${projectId}`);
    },
    createProject() {
      this.$router.push('/create_project');
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
    }
  },
  created() {
    this.fetchProjects();
  }
};
</script>

<style scoped>
.instructor-dashboard {
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

.logout-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: transparent;
  border: 1px solid #791912;
  border-radius: 6px;
  color: #791912;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background-color: #791912;
  color: white;
}

.dashboard-container {
  max-width: 1400px;
  margin: 6rem auto 2rem;
  padding: 0 2rem;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.dashboard-header h2 {
  color: #791912;
  font-size: 2rem;
  margin: 0;
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background-color: #d7a84e;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.create-btn:hover {
  background-color: #c29843;
  transform: translateY(-2px);
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.project-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid #eee;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}

.project-card-content {
  padding: 1.5rem;
}

.project-card h3 {
  color: #791912;
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.course-badge {
  display: inline-block;
  background-color: #f0f0f0;
  color: #666;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.project-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  color: #666;
  font-size: 0.9rem;
}

.project-stats span {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.view-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: transparent;
  border: 1px solid #791912;
  color: #791912;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-btn:hover {
  background-color: #791912;
  color: white;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #666;
}

.loading-state i,
.empty-state i {
  font-size: 3rem;
  color: #d7a84e;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 0 1rem;
  }

  .dashboard-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .projects-grid {
    grid-template-columns: 1fr;
  }
}
</style>
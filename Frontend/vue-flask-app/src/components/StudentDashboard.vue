<template>
  <div class="student-dashboard">
    <nav class="navbar">
      <div class="navbar-content">
        <div class="navbar-brand">
          <img src="/iitm.png" alt="IITM Logo" class="navbar-logo" />
          <span>IITM Project Hub</span>
        </div>
        <div class="navbar-right">
          <span class="welcome-text">Welcome, Student</span>
          <button @click="logout" class="logout-btn">
            <i class="fas fa-sign-out-alt"></i>
            Logout
          </button>
        </div>
      </div>
    </nav>

    <div class="dashboard-container">
      <div class="dashboard-header">
        <h2>My Projects</h2>
        <p class="subtitle">Track and manage your assigned projects</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <i class="fas fa-spinner fa-spin"></i>
        <p>Loading your projects...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="projects.length === 0" class="empty-state">
        <i class="fas fa-folder-open"></i>
        <p>No projects assigned yet</p>
      </div>

      <!-- Projects Grid -->
      <div v-else class="projects-grid">
        <div v-for="project in projects" :key="project.id" class="project-card">
          <div class="project-card-content">
            <h3 class="project-title">{{ project.title }}</h3>
            <p class="project-description">{{ project.problem }}</p>
            <div class="project-footer">
              <button @click="viewProjectInfo(project.id)" class="view-project-btn">
                <i class="fas fa-info-circle"></i>
                View Details
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
  name: 'StudentDashboard',
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
        const response = await fetch('http://127.0.0.1:5000/api/student_dashboard', {
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
    viewProjectInfo(projectId) {
      this.$router.push(`/myproject/${projectId}`);
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
    }
  },
  mounted() {
    this.fetchProjects();
  }
};
</script>

<style scoped>
.student-dashboard {
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

.navbar-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.welcome-text {
  color: #666;
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
  border-color: #791912;
}

.dashboard-container {
  max-width: 1200px;
  margin: 6rem auto 2rem;
  padding: 0 1.5rem;
}

.dashboard-header {
  margin-bottom: 2rem;
  text-align: center;
}

.dashboard-header h2 {
  color: #791912;
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666;
  font-size: 1.1rem;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  padding: 1rem 0;
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

.project-title {
  color: #791912;
  font-size: 1.25rem;
  margin-bottom: 1rem;
}

.project-description {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

.project-footer {
  border-top: 1px solid #eee;
  padding-top: 1rem;
}

.view-project-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #d7a84e;
  color: white;
  border: none;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-project-btn:hover {
  background-color: #c29843;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.loading-state i,
.empty-state i {
  font-size: 2rem;
  color: #d7a84e;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .navbar-content {
    flex-direction: column;
    gap: 1rem;
  }

  .dashboard-container {
    margin-top: 8rem;
  }

  .projects-grid {
    grid-template-columns: 1fr;
  }
}
</style>

<template>
  <div class="track-progress">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="navbar-content">
        <div class="navbar-brand">
          <img src="/iitm.png" alt="IITM Logo" class="navbar-logo" />
          <span>Student Progress Tracking</span>
        </div>
        <div class="nav-actions">
          <button @click="goBack" class="back-btn">
            <i class="fas fa-arrow-left"></i>
            Back to Project
          </button>
          <button @click="logout" class="logout-btn">
            <i class="fas fa-sign-out-alt"></i>
            Logout
          </button>
        </div>
      </div>
    </nav>

    <!-- Container -->
    <div class="container">
      <!-- Project Overview -->
      <div class="section-card">
        <div class="card-header">
          <h2>{{ project.title }}</h2>
        </div>
        <div class="problem-statement">
          <p>{{ project.problem }}</p>
        </div>
      </div>

      <!-- Milestones Progress -->
      <div class="section-card">
        <h3><i class="fas fa-tasks"></i> Milestone Progress</h3>
        <div class="milestones-grid">
          <div
            v-for="milestone in project.milestones"
            :key="milestone.id"
            class="milestone-card"
            :class="{ 'completed': milestone.status === 'Completed' }"
          >
            <div class="milestone-content">
              <div class="milestone-header">
                <span class="status-badge" :class="milestone.status.toLowerCase()">
                  {{ milestone.status }}
                </span>
              </div>
              <p class="milestone-text">{{ milestone.text }}</p>
              <p class="milestone-deadline">
                <i class="far fa-calendar-alt"></i>
                Due: {{ new Date(milestone.deadline).toLocaleDateString() }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Project Resources -->
      <div class="section-card">
        <h3><i class="fab fa-github"></i> Project Resources</h3>
        <div class="resources-grid">
          <div class="resource-item">
            <label>GitHub Repository</label>
            <div class="repo-url">
              <i class="fab fa-github"></i>
              <a :href="project.github_repo_url" target="_blank">{{ project.github_repo_url }}</a>
            </div>
          </div>
          <div class="resource-item">
            <label>Project Report</label>
            <div class="report-content">{{ project.project_report }}</div>
          </div>
        </div>
      </div>

      <!-- AI Evaluation Section -->
      <div class="section-card">
        <div class="card-header">
          <h3><i class="fas fa-robot"></i> AI Evaluation</h3>
          <button @click="getAIEvaluation" class="evaluate-btn" :disabled="isEvaluating">
            <i class="fas fa-sync-alt" :class="{ 'fa-spin': isEvaluating }"></i>
            {{ isEvaluating ? 'Evaluating...' : 'Get AI Evaluation' }}
          </button>
        </div>
        <div v-if="evaluationError" class="error-message">
          <i class="fas fa-exclamation-circle"></i>
          {{ evaluationError }}
        </div>
        <div v-if="aiEvaluation" class="evaluation-result markdown-content" v-html="renderedEvaluation"></div>
      </div>

      <!-- Commit Activity Section -->
      <div class="section-card">
        <div class="card-header">
          <h3><i class="fas fa-chart-line"></i> Commit Activity</h3>
          <button @click="resyncCommits" class="resync-btn">
            <i class="fas fa-sync-alt"></i> Resync Commits
          </button>
        </div>
        <!-- GitHub Commit History Component -->
        <GitHubCommitHistory :user-id=this.$route.params.studentId :repo-url="project.github_repo_url"  />
      </div>
    </div>
  </div>
</template>

<script>
import GitHubCommitHistory from '../components/GitHubCommitHistory.vue';
import { marked } from 'marked';

export default {
  name: 'TrackProgress',
  components: {
    GitHubCommitHistory
  },
  data() {
    return {
      project: {
        title: '',
        problem: '',
        milestones: [],
        github_repo_url: '',
        project_report: ''
      },
      aiEvaluation: null,
      isEvaluating: false,
      evaluationError: null
    };
  },
  methods: {
    async fetchProgress() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/track_progress/${this.$route.params.projectId}/${this.$route.params.studentId}`, {
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
        console.error('Error fetching progress:', error);
      }
    },
    async getAIEvaluation() {
      this.isEvaluating = true;
      this.evaluationError = null;

      try {
        const response = await fetch('http://127.0.0.1:5000/api/ai_eval', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({
            report: this.project.project_report,
            projectId: this.$route.params.projectId
          })
        });

        if (!response.ok) {
          throw new Error('Failed to get AI evaluation');
        }

        const data = await response.json();
        this.aiEvaluation = data.evaluation;
      } catch (error) {
        console.error('Error getting AI evaluation:', error);
        this.evaluationError = 'Failed to get AI evaluation. Please try again later.';
      } finally {
        this.isEvaluating = false;
      }
    },
    async resyncCommits() 
    {
      const urlParts = this.project.github_repo_url.split('/')
      const owner = urlParts[urlParts.length - 2]
      const repo = urlParts[urlParts.length - 1]
     
      const response = await fetch('http://127.0.0.1:5000/api/fetch-commits', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json',
             'Authorization': `Bearer ${localStorage.getItem('token')}`
           },
          body: JSON.stringify({
            owner: owner,
            repo: repo,
            userId : this.$route.params.studentId
          })
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.error || 'Failed to fetch commits')
        }
        else
        {
          window.location.reload();
        }
       

      
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
    },
    goBack() {
      this.$router.push(`/project/${this.$route.params.projectId}`);
    },
  },
  created() {
    this.fetchProgress();
  },
  computed: {
    renderedEvaluation() {
      return this.aiEvaluation ? marked(this.aiEvaluation) : '';
    }
  }
};
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.resync-btn {
  padding: 0.5rem 1.2rem;
  background-color: #d7a84e;
  border: none;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.resync-btn:hover {
  background-color: #c29843;
}

.resync-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.track-progress {
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
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.card-header h2,
.card-header h3 {
  color: #791912;
  margin: 0;
}
h3 {
  color: #791912;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.milestones-grid {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

.milestone-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid #eee;
  transition: all 0.3s ease;
}

.milestone-card.completed {
  border-left: 4px solid #28a745;
  background-color: #f8fff8;
}

.milestone-header {
  margin-bottom: 1rem;
}

.status-badge {
  display: inline-flex;
  align-items: center;
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

.milestone-text {
  color: #444;
  margin-bottom: 0.75rem;
  line-height: 1.5;
}

.milestone-deadline {
  color: #666;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.resources-grid {
  display: grid;
  gap: 2rem;
}

.resource-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.resource-item label {
  color: #666;
  font-weight: 500;
}

.repo-url {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 6px;
}

.repo-url a {
  color: #0366d6;
  text-decoration: none;
  word-break: break-all;
}

.repo-url a:hover {
  text-decoration: underline;
}

.report-content {
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 6px;
  color: #444;
  line-height: 1.6;
  min-height: 100px;
}

.evaluate-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background-color: #d7a84e;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.evaluate-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.evaluate-btn:not(:disabled):hover {
  background-color: #c29843;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background-color: #fff5f5;
  color: #dc3545;
  border-radius: 6px;
  margin-bottom: 1rem;
}

.evaluation-result {
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-radius: 6px;
  color: #444;
  line-height: 1.6;
}

.markdown-content {
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-radius: 6px;
  color: #444;
  line-height: 1.6;
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3) {
  color: #791912;
  margin: 1rem 0;
}

.markdown-content :deep(p) {
  margin-bottom: 1rem;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}

.markdown-content :deep(li) {
  margin-bottom: 0.5rem;
}

.markdown-content :deep(code) {
  background-color: #eee;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: monospace;
}

.markdown-content :deep(pre) {
  background-color: #2d2d2d;
  color: #fff;
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
  margin: 1rem 0;
}

.markdown-content :deep(blockquote) {
  border-left: 4px solid #d7a84e;
  padding-left: 1rem;
  margin: 1rem 0;
  color: #666;
}

.markdown-content :deep(a) {
  color: #0366d6;
  text-decoration: none;
}

.markdown-content :deep(a:hover) {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
  
  .milestones-grid {
    grid-template-columns: 1fr;
  }

  .card-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .evaluate-btn {
    width: 100%;
  }
}
</style>


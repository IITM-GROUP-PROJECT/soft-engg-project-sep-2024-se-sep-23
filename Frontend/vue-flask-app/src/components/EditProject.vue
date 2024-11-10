<template>
  <div class="project-edit">
    <nav class="navbar">
      <div class="navbar-content">
        <div class="navbar-brand">
          <img src="/iitm.png" alt="IITM Logo" class="navbar-logo" />
          <span>Edit Project</span>
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
      <div v-if="loading" class="loading-state">
        <i class="fas fa-spinner fa-spin"></i>
        <p>Loading project details...</p>
      </div>

      <div v-else class="content">
        <!-- Project Info Card -->
        <div class="section-card project-info-card">
          <div class="problem-statement">
            <h2>Project Title</h2>
            <input v-model="project.title" class="input-title" placeholder="Project Title" />
          </div>
          <div class="problem-statement">
            <h3>Problem Statement</h3>
            <textarea v-model="project.problem" class="input-problem"
              placeholder="Describe the problem statement here..."></textarea>
          </div>
        </div>

        <!-- Milestones Section -->
        <div class="section-card">
          <h3><i class="fas fa-tasks"></i> Project Milestones</h3>
          <div class="milestones-list">
            <div v-for="(milestone, index) in project.milestones" :key="milestone.id || index" class="milestone-card">
              <input v-model="milestone.title" class="milestone-input" placeholder="Milestone title" />
              <input v-model="milestone.description" class="milestone-input" placeholder="Milestone description" />
              <input type="date" v-model="milestone.deadline" class="milestone-deadline-input" />
              <button @click="removeMilestone(index)" class="remove-btn">Remove</button>
            </div>
          </div>
          <br>
          <!-- Add Milestone Button -->
          <button @click="addMilestone" class="add-milestone-btn">Add Milestone</button>
        </div>

        <!-- Students Section -->
        <div class="section-card">
          <h3><i class="fas fa-users"></i> Assign Students</h3>

          <!-- Search Bar -->
          <div class="search-container">
            <input type="text" v-model="searchQuery" class="search-bar" placeholder="Search students...">
            <i class="fas fa-search search-icon"></i>
          </div>

          <!-- Students List -->
          <div class="students-list">
            <div v-for="student in filteredStudents" :key="student.id" class="student-item">
              <label class="checkbox-container">
                <input type="checkbox" :value="student.id" v-model="selectedStudents">
                <span class="student-email">{{ student.email }}</span>
              </label>
            </div>
          </div>
        </div>

        <button @click="saveChanges" class="save-btn">Save Changes</button>
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
        milestones: [],
        students: []
      },
      students_add: [],  // Unassigned students (for potential assignment)
      selectedStudents: [], // To track selected students for assignment
      searchQuery: '', // Search query to filter students
      loading: true
    };
  },
  computed: {
    filteredStudents() {
      if (!this.searchQuery) {
        return this.students_add;
      }
      return this.students_add.filter(student =>
        student.email.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
    async saveChanges() {
      try {
        // Clean up empty milestones (check for non-empty title, description, and deadline)
        const cleanedMilestones = this.project.milestones.filter(milestone =>
          milestone.title.trim() !== '' && milestone.description.trim() !== '' && milestone.deadline
        );

        // Prepare the updated project object with the current milestones and selected students
        const updatedProject = {
          ...this.project,
          milestones: cleanedMilestones,
          students: this.selectedStudents // Include selected students
        };

        // Send the updated project to the backend
        const response = await fetch(`http://127.0.0.1:5000/api/update_project/${this.$route.params.projectId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(updatedProject)
        });

        if (!response.ok) throw new Error('Failed to save changes');
        alert('Project updated successfully');
        this.$router.push('/instructor_dashboard');
      } catch (error) {
        console.error('Error saving project:', error);
      }
    },
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
        if (!response.ok) throw new Error('Failed to fetch project details');
        const data = await response.json();

        this.project = data;
        this.students_add = data.students_add; // Get all students for assignment
        this.selectedStudents = data.students.map(student => student.id); // Pre-select assigned students
      } catch (error) {
        console.error('Error fetching project details:', error);
      } finally {
        this.loading = false;
      }
    },
    addMilestone() {
      this.project.milestones.push({ title: '', description: '', deadline: '' });
    },
    removeMilestone(index) {
      this.project.milestones.splice(index, 1);
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
/* Retained styles from the original component */
.search-container {
  position: relative;
  margin-bottom: 20px;
}

.search-bar {
  width: 100%;
  padding: 10px 35px 10px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.search-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.students-list {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
}

.student-item {
  padding: 8px;
  border-bottom: 1px solid #eee;
}

.student-item:last-child {
  border-bottom: none;
}

.checkbox-container {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.checkbox-container input {
  margin-right: 10px;
}

.student-email {
  margin-left: 8px;
}

/* Custom checkbox styling */
.checkmark {
  width: 18px;
  height: 18px;
  border: 2px solid #4a90e2;
  border-radius: 3px;
  margin-right: 10px;
}

.checkbox-container input:checked + .checkmark {
  background-color: #4a90e2;
}
/* Project Edit Styles */
.input-title,
.input-problem,
.milestone-input,
.student-email-input {
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.milestone-deadline-input {
  padding: 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.add-milestone-btn,
.add-student-btn,
.save-btn,
.remove-btn {
  padding: 0.5rem 1rem;
  background-color: #791912;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: -1rem;
}

.save-btn {
  background-color: #4caf50;
}

.remove-btn {
  background-color: #dc3545;
  margin-left: 1rem;
}

.save-btn:hover,
.add-milestone-btn:hover,
.add-student-btn:hover,
.remove-btn:hover {
  opacity: 0.9;
}

/* Retained styles from the original code */
.project-edit {
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
  color: #333;
}
</style>
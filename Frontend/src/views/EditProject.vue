<template>
  <div class="edit-project">
    <nav class="navbar">
      <div class="navbar-content">
        <div class="navbar-brand">
          <img src="/iitm.png" alt="IITM Logo" class="navbar-logo" />
          <span>Edit Project</span>
        </div>
        <div class="nav-actions">
          <button @click="goBack" class="back-btn">
            <i class="fas fa-arrow-left"></i>
            Back to Project Details
          </button>
          <button @click="logout" class="logout-btn">
            <i class="fas fa-sign-out-alt"></i>
            Logout
          </button>
        </div>
      </div>
    </nav>

    <div class="container">
      <div class="form-card" v-if="project">
        <form @submit.prevent="updateProject">
          <!-- Project Details -->
          <div class="form-section">
            <h3>Project Details</h3>
            <div class="form-group">
              <label for="title">Project Title</label>
              <input type="text" v-model="project.title" id="title" required />
            </div>
            <div class="form-group">
              <label for="problem">Project Problem Statement</label>
              <textarea v-model="project.problem" id="problem" rows="4" required></textarea>
            </div>
          </div>

          <!-- Course Selection -->
          <div class="form-section">
            <h3>Course Information</h3>
            <div class="form-group">
              <label for="courseSelection">Select Course</label>
              <select v-model="selectedCourse" id="courseSelection" required>
                <option v-for="course in courses" :key="course.id" :value="course.id">
                  {{ course.name }}
                </option>
                <option value="new">+ Add New Course</option>
              </select>
            </div>
            <div v-if="selectedCourse === 'new'" class="form-group">
              <label for="newCourse">New Course Name</label>
              <input type="text" v-model="newCourseName" id="newCourse" required />
            </div>
          </div>

          <!-- Milestones -->
          <div class="form-section">
            <div class="milestone-header">
              <h3>Project Milestones</h3>
              <button type="button" @click="addMilestone" class="add-milestone-btn">
                <i class="fas fa-plus"></i> Add Milestone
              </button>
            </div>
            <div class="milestones-container">
              <div v-for="(milestone, index) in project.milestones" :key="index" class="milestone-card">
                <div class="milestone-number">#{{ index + 1 }}</div>
                <div class="milestone-inputs">
                  <input type="text" v-model="milestone.title" placeholder="Milestone Title" required />
                  <input type="text" v-model="milestone.description" placeholder="Milestone Description" required />
                  <input type="date" v-model="milestone.deadline" required />
                </div>
                <button type="button" @click="removeMilestone(index)" class="remove-btn">
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
          </div>

          <!-- Student Assignment -->
          <div class="form-section">
            <h3>Assign New Students</h3>
            <div class="students-grid">
              <div v-for="student in unassignedStudents" :key="student.id" class="student-item">
                <input
                  type="checkbox"
                  :id="'student-' + student.id"
                  :value="student.id"
                  v-model="selectedNewStudents"
                />
                <label :for="'student-' + student.id">{{ student.email }}</label>
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
      project: null,
      courses: [],
      unassignedStudents: [],
      selectedNewStudents: [],
      selectedCourse: '',
      newCourseName: '' 
    }
  },
  async created() {
    await this.fetchProjectData()
    await this.fetchCourses()
  },
  methods: {
    async fetchProjectData() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/edit_project/${this.$route.params.projectId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        })
        const data = await response.json()
        this.project = data.project
        this.selectedCourse = data.project.course_id // Set initial course
        this.unassignedStudents = data.unassigned_students
      } catch (error) {
        console.error('Error fetching project:', error)
      }
    },
    async fetchCourses() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/courses', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.courses = await response.json()
      } catch (error) {
        console.error('Error fetching courses:', error)
      }
    },
    addMilestone() {
      this.project.milestones.push({
        title: '',
        description: '',
        deadline: ''
      })
    },
    removeMilestone(index) {
      this.project.milestones.splice(index, 1)
    },
    async updateProject() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/edit_project/${this.project.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({
            ...this.project,
            student_ids: [...this.project.assigned_students, ...this.selectedNewStudents],
            new_course: this.selectedCourse === 'new',
            course_id: this.selectedCourse === 'new' ? null : this.selectedCourse,
            course_name: this.selectedCourse === 'new' ? this.newCourseName : null
          })
        })
        
        if (response.ok) {
          alert('Project updated successfully')
          this.$router.push('/instructor_dashboard')
        } else {
          throw new Error('Failed to update project')
        }
      } catch (error) {
        console.error('Error updating project:', error)
        alert('Failed to update project')
      }
    },
    logout() {
      localStorage.removeItem('token')
      this.$router.push('/')
    },
    goBack() {
      this.$router.push(`/project/${this.project.id}`);
    }
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

.form-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  border-top: 4px solid #791912;
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

input, textarea, select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #eee;
  border-radius: 6px;
  transition: all 0.3s ease;
}

input:focus, textarea:focus, select:focus {
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

.add-milestone-btn {
  background: #d7a84e;
  border: none;
  color: white;
  padding: 0.75rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
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
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.submit-btn:hover {
  background: #8a1c14;
}

.students-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.student-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border: 1px solid #eee;
  border-radius: 6px;
}

.student-item label {
  margin: 0;
  cursor: pointer;
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
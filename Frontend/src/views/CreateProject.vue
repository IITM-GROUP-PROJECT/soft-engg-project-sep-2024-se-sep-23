<template>
  <div class="create-project">
    <nav class="navbar">
      <div class="navbar-content">
        <div class="navbar-brand">
          <img src="/iitm.png" alt="IITM Logo" class="navbar-logo" />
          <span>Create New Project</span>
        </div>
        <button @click="logout" class="logout-btn">
          <i class="fas fa-sign-out-alt"></i>
          Logout
        </button>
      </div>
    </nav>

    <div class="container">
      <div class="form-card">
        <form @submit.prevent="createProject">
          <div class="form-section">
            <h3>Project Details</h3>
            <div class="form-group">
              <label for="title">Project Title</label>
              <input type="text" v-model="title" id="title" required />
            </div>
            <div class="form-group">
              <label for="problem">Project Problem Statement</label>
              <textarea v-model="problem" id="problem" rows="4" required></textarea>
            </div>
          </div>

          <div class="form-section">
            <h3>Course Information</h3>
            <div class="form-group">
              <label for="courseSelection">Select Course</label>
              <select v-model="selectedCourse" id="courseSelection" required>
                <option value="">Select a course</option>
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

          <div class="form-section">
            <h3>Assign Students</h3>
            <div class="form-group">
              <label for="students">Upload Students Details in CSV</label>
              <input
                type="file"
                id="student-upload"
                @change="handleFileUpload"
                accept=".csv"
                required
              />
            </div>
          </div>

          <div class="form-section">
            <div class="milestone-header">
              <h3>Project Milestones</h3>
              <button
                type="button"
                @click="addMilestone"
                class="add-milestone-btn"
              >
                <i class="fas fa-plus"></i> Add Milestone
              </button>
            </div>
            <div class="milestones-container">
              <div
                v-for="(milestone, index) in milestones"
                :key="index"
                class="milestone-card"
              >
                <div class="milestone-number">#{{ index + 1 }}</div>
                <div class="milestone-inputs">
                  <input
                    type="text"
                    v-model="milestone.title"
                    placeholder="Milestone Title"
                    required
                  />
                  <input
                    type="text"
                    v-model="milestone.description"
                    placeholder="Milestone Description"
                    required
                  />
                  <input type="date" v-model="milestone.deadline" required />
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
              <i class="fas fa-check"></i> Create Project
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import Papa from 'papaparse'; // Make sure to install the papaparse library

export default {
  name: "CreateProject",
  data() {
    return {
      title: "",
      problem: "",
      students: [],
      selectedStudents: [],
      milestones: [{ title: "", description: "", deadline: "" }],
      courses: [],
      selectedCourse: "",
      newCourseName: "",
    };
  },
  methods: {
    async fetchStudents() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/students", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        this.students = data;
      } catch (error) {
        console.error("Error fetching students:", error);
      }
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const content = e.target.result;
          this.parseCSV(content);
        };
        reader.readAsText(file);
      }
    },
    parseCSV(content) {
      Papa.parse(content, {
        complete: (result) => {
          // Assuming first column contains email addresses
          this.selectedStudents = result.data.map(row => row[0].trim()).filter(Boolean);
        },
        header: false, // Set to true if the CSV has headers
      });
    },
    addMilestone() {
      this.milestones.push({ title: "", description: "", deadline: "" });
    },
    removeMilestone(index) {
      this.milestones.splice(index, 1);
    },
    async fetchCourses() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/courses", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        if (response.ok) {
          this.courses = await response.json();
        }
      } catch (error) {
        console.error("Error fetching courses:", error);
      }
    },
    async createProject() {
      try {
        // First get student IDs for the emails
        const emailResponse = await fetch("http://127.0.0.1:5000/api/get_student_ids", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify({ emails: this.selectedStudents })
        });

        if (!emailResponse.ok) {
          throw new Error("Failed to process student emails");
        }

        const emailData = await emailResponse.json();
        
        // Send registration reminders for unregistered emails
        if (emailData.unregistered_emails.length > 0) {
          await fetch("http://127.0.0.1:5000/api/send_reminder_to_register", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
            body: JSON.stringify({ emails: emailData.unregistered_emails })
          });
        }
        
         // Create project with registered student IDs
         const projectData = {
          title: this.title,
          problem: this.problem,
          student_ids: emailData.registered_student_ids,
          milestones: this.milestones,
          new_course: this.selectedCourse === 'new',
          course_id: this.selectedCourse === 'new' ? null : this.selectedCourse,
          course_name: this.selectedCourse === 'new' ? this.newCourseName : null
        };

        const response = await fetch("http://127.0.0.1:5000/api/create_project", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify(projectData),
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        alert(data.msg);
        this.$router.push("/instructor_dashboard");
      } catch (error) {
        console.error("Error creating project:", error);
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/");
    },
  },
  created() {
    this.fetchStudents();
    this.fetchCourses();
  },
};
</script>

<style scoped>
.create-project {
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

select[multiple] {
  height: 200px;
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

.logout-btn, .secondary-btn, .add-milestone-btn, .remove-btn, .submit-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn {
  background: transparent;
  border: 1px solid #791912;
  color: #791912;
}

.logout-btn:hover {
  background: #791912;
  color: white;
}

.secondary-btn {
  background: #f8f9fa;
  border: 1px solid #ddd;
  color: #666;
}

.secondary-btn:hover {
  background: #eee;
}

.add-milestone-btn {
  background: #d7a84e;
  border: none;
  color: white;
}

.add-milestone-btn:hover {
  background: #c29843;
}

.remove-btn {
  background: transparent;
  border: none;
  color: #dc3545;
  padding: 0.5rem;
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

select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #eee;
  border-radius: 6px;
  transition: all 0.3s ease;
}

select:focus {
  outline: none;
  border-color: #791912;
}

</style>
<template>
    <div class="instructor-dashboard">
      <!-- Navigation Bar -->
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark w-100 mb-3">
        <a class="navbar-brand" href="/">Project Management System</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ml-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/instructor_login">Logout</router-link>
            </li>
          </ul>
        </div>
      </nav>
  
      <!-- Dashboard Content -->
      <div class="container mt-5">
        <h2>Instructor Dashboard</h2>
        <div class="row mt-3">
          <div class="col-md-3" v-for="course in courses" :key="course.id">
            <div class="card mb-3">
              <div class="card-body">
                <h5 class="card-title">{{ course.title }}</h5>
                <p class="card-text">Code: {{ course.code }}</p>
                <p class="card-text">Dates: {{ course.dateRange }}</p>
                <p class="card-text">Students Enrolled: {{ course.students }}</p>
                <button class="btn btn-primary" @click="viewCourse(course.id)">View Course</button>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Create Project Button -->
      <button class="create-project-btn" @click="createProject">
        <i class="fas fa-plus"></i> Create Project
      </button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        courses: [
          { id: 1, code: "BUS280", title: "Business Law", dateRange: "08/29 - 11/13 2017", students: 15 },
          { id: 2, code: "BUS320", title: "Operations Management", dateRange: "08/28 - 11/13 2017", students: 20 },
          { id: 3, code: "BUS340", title: "Leadership and Management", dateRange: "09/02 - 11/13 2017", students: 17 },
          { id: 3, code: "BUS340", title: "Leadership and Management 2", dateRange: "09/02 - 11/13 2017", students: 17 }
          // Add more course data as needed
        ],
      };
    },
    methods: {
      viewCourse(courseId) {
        // Redirect to course details page (you can replace this with actual route logic)
        alert(`Navigating to course ID: ${courseId}`);
      },
      createProject() {
        // Logic to create a new project
        alert("Create project clicked");
      }
    }
  };
  </script>
  
<style scoped>
.instructor-dashboard .navbar {
  margin-bottom: 20px;
  background-color: #343a40;
  padding: 1rem;
}

.instructor-dashboard .navbar-brand {
  color: #ffffff;
  font-weight: bold;
}

.instructor-dashboard .navbar-nav .nav-link {
  color: #ffffff;
  margin-right: 1rem;
}

.instructor-dashboard .container {
  max-width: 100%;
  margin: 50px auto; /* Center container horizontally */
  display: flex;
  flex-direction: column;
  /* align-items: center; */
}

.instructor-dashboard .row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center; /* Center the cards */
  gap: 20px; /* Adjust gap between cards */
}

.instructor-dashboard .col-md-4 {
  flex: 0 0 300px; /* Set a fixed width for each card */
}


.instructor-dashboard h2 {
  text-align: center;
  margin-bottom: 20px;
  font-weight: bold;
  color: #333;
}



.instructor-dashboard .card {
  width: 100%;
  max-width: 100%;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.instructor-dashboard .card .card-body {
  padding: 20px;
}

.instructor-dashboard .card-title {
  font-size: 1.25rem;
  font-weight: bold;
  color: #0056b3;
}

.instructor-dashboard .card-text {
  color: #000000;
  margin-bottom: 10px;
  font-size: 0.9rem;
}

.instructor-dashboard .btn-primary {
  background-color: #007bff;
  border: none;
  width: 100%;
  font-size: 0.9rem;
}
  </style>
  
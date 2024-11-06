<template>
  <div class="d-flex flex-column min-vh-100">
    <!-- Navbar covering full width -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark w-100 mb-3">
      <a class="navbar-brand" href="/">Project Management System</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ml-auto"> <!-- Use ml-auto to push items to the right -->
          <li class="nav-item">
            <router-link class="nav-link" to="/instructor_login">Instructor Login</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/student_login">Student Login</router-link>
          </li>
        </ul>
      </div>
    </nav>

    <div class="d-flex flex-grow-1">
      <!-- Left Sidebar -->
      <div class="sidebar text-dark p-4 d-flex flex-column justify-content-start">
        <h2 class="sidebar-title">Get Started</h2>
        <div class="sidebar-links">
          <div class="card mb-3">
            <div class="card-body text-center">
              <h5 class="card-title">Instructor</h5>
              <p class="card-text">Manage your projects and students effectively.</p>
              <router-link class="btn btn-primary btn-block" to="/instructor_signup">Instructor Signup</router-link>
            </div>
          </div>
          <div class="card mb-3">
            <div class="card-body text-center">
              <h5 class="card-title">Student</h5>
              <p class="card-text">Submit your projects and track your progress.</p>
              <router-link class="btn btn-success btn-block" to="/student_signup">Student Signup</router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content Area with full background image -->
      <div class="flex-grow-1 welcome-section d-flex flex-column align-items-start justify-content-start text-white p-4">
        <h2 class="title">Welcome to the Project Management System</h2>
        <p class="description">Efficiently manage projects and track your progress!</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
};
</script>

<style scoped>
/* Global styles */
body {
  background-color: white; /* Light background for a clean look */
  font-family: 'Arial', sans-serif;
  margin: 0;
  padding: 0;
 
 /* Simple and modern font */
}



.navbar {
  background-color: #343a40; /* Darker navbar for contrast */
  width: 100%; /* Ensures navbar covers full width */
  margin-bottom: 20px;
  padding-left: 20px;
  padding-right: 20px;
 /* Added bottom margin */
}

.nav-link {
  font-weight: bold; /* Bold links for clarity */
  padding: 15px; /* Increase padding for better click area */
  
}

.sidebar {
  width: 300px; /* Fixed width for sidebar */
  background-color: #e9e9e9; /* Lighter grey for a cleaner look */
  color: #000000; /* Dark text color for contrast */
  padding: 20px; /* Padding for inner spacing */
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* Align content to top */
  margin-right: 20px;
  margin-left: 20px; /* Space between sidebar and content */
  min-height: 80vh; /* Ensures sidebar is tall enough */
  border-radius: 10px; /* Rounded corners for a softer look */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow */
}

.sidebar-title {
  font-size: 1.8rem; /* Larger title font size */
  margin-bottom: 20px; /* Space below title */
  font-weight: bold; /* Bold title */
  text-align: center; /* Center align title */
  color: #4795e9; /* Blue color for the title */
}

.sidebar-links {
  margin-top: 20px; /* Space above links */
}

.card {
  background-color: #d1d5e2; /* White background for cards */
  border-radius: 10px; /* Rounded corners for cards */
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1); /* Soft shadow for cards */
  transition: transform 0.3s ease; /* Animation on hover */
  margin-bottom: 15px; /* Space between cards */
}

.card:hover {
  transform: translateY(-5px); /* Lift effect on hover */
}

.card .card-title {
  color: #007bff; /* Blue color for card titles */
  font-weight: bold; /* Bold titles */
}

.card .btn {
  padding: 10px; /* Padding for buttons */
  font-weight: bold; /* Bold text for buttons */
  border-radius: 5px; /* Rounded button corners */
}

.card .btn-primary {
  background-color: #28a745; /* Primary color for button */
  border: none; /* Remove border */
}

.card .btn-success {
  background-color: #28a745; /* Success color for button */
  border: none; /* Remove border */
}

/* Optional hover effects for buttons */
.card .btn:hover {
  opacity: 0.9; /* Slightly darken button on hover */
}

.welcome-section {
  background-image: url('data:image/jpeg;base64,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');
  background-size: cover; /* Cover the section */
  background-position: center; /* Center the image */
  background-repeat: no-repeat; /* Prevent image repetition */
  min-height: 100vh; /* Ensures it takes up the full height */
  margin-right: 20px;
  color: rgb(188, 216, 137); /* Text color */
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7); /* Shadow for text contrast */
}

.title {
  font-size: 2.5rem; /* Prominent title */
  margin-top: 20px; /* Margin above title */
  margin-left: 70px;
}

.description {
  font-size: 1.3rem; /* Font size for description */
  margin-top: 10px; /* Space above description */
  max-width: 600px; /* Limit width for better readability */
  margin-left: 190px;
}
</style>

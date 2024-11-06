<template>
    <div class="student-login">
      <!-- Navigation Bar -->
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark w-100 mb-3">
        <a class="navbar-brand" href="#">Project Management System</a>
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
  
      <!-- Login Form -->
      <div class="container mt-5">
        <h2>Student Login</h2>
        <form @submit.prevent="login">
          <div class="form-group">
            <input type="text" v-model="username" class="form-control" placeholder="Username" required />
          </div>
          <div class="form-group">
            <input type="password" v-model="password" class="form-control" placeholder="Password" required />
          </div>
          <button type="submit" class="btn btn-primary">Login</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: '',
        password: ''
      };
    },
    methods: {
      login() {
        fetch('/student_login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data.access_token) {
            localStorage.setItem('token', data.access_token);
            alert('Login successful');
          } else {
            alert('Login failed');
          }
        })
        .catch(error => {
          console.error('Error during login:', error);
          alert('Login failed');
        });
      }
    }
  };
  </script>
  
  <style scoped>
  .student-login .container {
    max-width: 400px; /* Limit the width of the form */
    margin: auto; /* Center the form horizontally */
    padding: 20px; /* Add some padding inside the form */
    border: 1px solid #ccc; /* Light gray border */
    border-radius: 8px; /* Rounded corners */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
    background-color: #ffffff; /* White background */
  }
  
  .student-login .form-group {
    margin-bottom: 15px; /* Space between form fields */
  }
  
  .student-login .form-control {
    height: calc(2.25rem + 2px); /* Set height for input fields */
    padding: 0.375rem 0.75rem; /* Add padding inside input fields */
    border: 1px solid #ced4da; /* Default border color */
    border-radius: 0.25rem; /* Rounded input fields */
  }
  
  .student-login .btn {
    width: 100%; /* Full width button */
    padding: 0.5rem; /* Add some padding */
    font-size: 1rem; /* Set font size */
    border-radius: 0.25rem; /* Rounded button */
  }
  
  .student-login h2 {
    text-align: center; /* Center the heading */
    margin-bottom: 20px; /* Space below the heading */
  }
  
  .student-login .mt-5 {
    margin-top: 3rem; /* Margin top for spacing */
  }
  </style>
  
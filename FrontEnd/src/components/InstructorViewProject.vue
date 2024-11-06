<template>
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
    <div class="project-page container mt-5">
      <h2>Project Overview</h2>
  
      <!-- Projects Table -->
      <table class="table mt-4">
        <thead>
          <tr>
            <th>Milestone</th>
            <th>Deadline</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(milestone, index) in project.milestones" :key="index">
            <td>{{ milestone.description }}</td>
            <td>{{ milestone.deadline }}</td>
            <td>
              <button class="btn btn-success btn-sm" @click="editMilestone(index)">Edit</button>
              <button class="btn btn-danger btn-sm ml-2" @click="deleteMilestone(index)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <!-- Track Students Button -->
      <div class="track-students-btn">
        <button class="btn btn-primary" @click="trackStudents">Track Students</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { reactive } from 'vue';
  
  const project = reactive({
    name: 'Sample Project',
    milestones: [
      { description: 'Milestone 1', deadline: '2023-12-01' },
      { description: 'Milestone 2', deadline: '2024-01-15' },
      // Add more milestones as needed
    ],
  });
  
  function editMilestone(index) {
    alert(`Editing milestone: ${project.milestones[index].description}`);
    // Implement actual edit logic here
  }
  
  function deleteMilestone(index) {
    if (confirm('Are you sure you want to delete this milestone?')) {
      project.milestones.splice(index, 1);
    }
  }
  
  function trackStudents() {
    alert('Tracking students for this project.');
    // Implement actual tracking logic here
  }
  </script>
  
  <style scoped>
  .container {
    max-width: 800px;
    margin: 0 auto;
  }
  
  .table {
    width: 100%;
    margin-top: 20px;
  }
  
  .track-students-btn {
    display: flex;
    justify-content: center;
    margin-top: 30px;
  }
  
  .btn-primary {
    width: 200px;
    font-weight: bold;
  }
  
  .btn-danger {
    margin-left: 10px;
  }
  </style>
  
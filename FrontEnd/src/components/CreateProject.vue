<template>
    <div class="create-project">
      <!-- Navbar -->
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark w-100 mb-3">
        <a class="navbar-brand" href="/">Project Management System</a>
        <button
          class="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ml-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/instructor_dashboard">Back to Dashboard</router-link>
            </li>
          </ul>
        </div>
      </nav>
  
      <!-- Project Form -->
      <div class="container mt-5">
        <h2>Create New Project</h2>
        <br />
        <form @submit.prevent="createProject">
          <div class="form-group">
            <label for="projectTitle"><h5>Project Title</h5></label>
            <input
              type="text"
              v-model="projectTitle"
              id="projectTitle"
              class="form-control"
              placeholder="Enter Project Title"
              required
            />
          </div>
          <br />
          <div class="form-group">
            <label for="projectDescription"><h5>Project Description</h5></label>
            <input
              type="text"
              v-model="projectDescription"
              id="projectTitle"
              class="form-control"
              placeholder="Enter Project Description"
              required
            />
          </div>
          <br>
          <div
            v-for="(milestone, index) in milestones"
            :key="index"
            class="milestone-group mb-3"
          >
            <h5>Milestones</h5>
            <textarea
              v-model="milestone.description"
              :id="'milestone-' + index"
              class="form-control"
              placeholder="Enter milestone description"
              required
              @input="autoResize"
              rows="1"
            ></textarea>
  
            <div class="form-group mt-2">
              <label :for="'deadline-' + index"><h5>Deadline</h5></label>
              <input
                type="date"
                v-model="milestone.deadline"
                :id="'deadline-' + index"
                class="form-control"
                required
              />
            </div>
  
            <!-- Remove milestone button -->
            <button
              type="button"
              class="btn btn-danger btn-sm remove-btn"
              @click="removeMilestone(index)"
            >
              Remove
            </button>
          </div>
  
          <!-- Button group -->
          <div class="button-group">
            <button type="button" class="btn btn-secondary" @click="addMilestone">
              + Add Milestone
            </button>
  
            <button type="submit" class="btn btn-primary">
              Create Project
            </button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const projectTitle = ref('');
  const milestones = ref([{ description: '', deadline: '' }]);
  
  function addMilestone() {
    milestones.value.push({ description: '', deadline: '' });
  }
  
  function removeMilestone(index) {
    milestones.value.splice(index, 1);
  }
  
  function createProject() {
    const projectData = {
      title: projectTitle.value,
      milestones: milestones.value.filter(
        (milestone) =>
          milestone.description.trim() !== '' && milestone.deadline
      ),
    };
  
    console.log('Project Created:', projectData);
    alert('Project created successfully!');
  
    // Reset form
    projectTitle.value = '';
    milestones.value = [{ description: '', deadline: '' }];
  }
  
  function autoResize(event) {
    const textarea = event.target;
    textarea.style.height = 'auto';
    textarea.style.height = `${textarea.scrollHeight}px`;
  }
  </script>
  
  <style scoped>
  .create-project .container {
    text-align: left;
    max-width: 600px;
  }
  
  .create-project h2 {
    margin-bottom: 10px;
    text-align: center;
  }

  .milestone-group {
    position: relative;
    margin-bottom: 20px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    text-align: left;
  }
  
  .remove-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 12px;
  }
  
  .button-group {
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: 10px;
    margin-top: 20px;
  }
  
  .btn-secondary,
  .btn-primary {
    width: 100%;
    font-weight: bold;
  }
  </style>
  
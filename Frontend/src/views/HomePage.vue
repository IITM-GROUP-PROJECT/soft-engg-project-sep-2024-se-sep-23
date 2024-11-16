<template>
  <div class="home-container">
    <!-- Hero Section -->
    <div class="hero-section">
      <img src="/iitm.png" alt="IITM Logo" class="iitm-logo" />
      <h1>Project Management System</h1>
      <p class="hero-text">
        Empowering IITM instructors and students with seamless project collaboration
      </p>
    </div>

    <!-- Features Section -->
    <div class="features-container">
      <div class="feature-box">
        <i class="fas fa-tasks"></i>
        <h3>Project Tracking</h3>
        <p>Create and manage projects with detailed milestones</p>
      </div>
      <div class="feature-box">
        <i class="fas fa-chart-line"></i>
        <h3>Progress Analytics</h3>
        <p>Monitor student progress through commit history</p>
      </div>
      <div class="feature-box">
        <i class="fas fa-users"></i>
        <h3>Collaboration</h3>
        <p>Seamless interaction between instructors and students</p>
      </div>
    </div>

    <!-- Login/Signup Section -->
    <div class="auth-section">
      <h2>Get Started</h2>
      <div class="auth-buttons">
        <div class="auth-column">
          <h3>For Instructors</h3>
          <router-link to="/instructor-login" class="auth-button instructor">
            Instructor Login
          </router-link>
          <router-link to="/instructor-signup" class="auth-button instructor-outline">
            Create Instructor Account
          </router-link>
        </div>
        <div class="auth-column">
          <h3>For Students</h3>
          <router-link to="/student-login" class="auth-button student">
            Student Login
          </router-link>
          <router-link to="/student-signup" class="auth-button student-outline">
            Create Student Account
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage'
};
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9));
}

.hero-section {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #791912 0%, #8a1c14 100%);
  color: white;
}

.iitm-logo {
  height: 100px;
  margin-bottom: 2rem;
}

.hero-section h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.hero-text {
  font-size: 1.2rem;
  max-width: 600px;
  margin: 0 auto;
  color: #d7a84e;
}

.features-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  padding: 4rem 2rem;
  background-color: #f8f9fa;
}

.feature-box {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-box:hover {
  transform: translateY(-5px);
}

.feature-box i {
  font-size: 2rem;
  color: #791912;
  margin-bottom: 1rem;
}

.feature-box h3 {
  color: #791912;
  margin-bottom: 1rem;
}

.auth-section {
  padding: 4rem 2rem;
  text-align: center;
}

.auth-section h2 {
  color: #791912;
  margin-bottom: 3rem;
}

.auth-buttons {
  display: flex;
  justify-content: center;
  gap: 3rem;
  flex-wrap: wrap;
}

.auth-column {
  flex: 1;
  min-width: 250px;
  max-width: 400px;
}

.auth-column h3 {
  color: #791912;
  margin-bottom: 1.5rem;
}

.auth-button {
  display: block;
  padding: 1rem 2rem;
  margin: 1rem 0;
  border-radius: 5px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.instructor {
  background-color: #791912;
  color: white;
}

.instructor:hover {
  background-color: #8a1c14;
}

.instructor-outline {
  border: 2px solid #791912;
  color: #791912;
}

.instructor-outline:hover {
  background-color: #791912;
  color: white;
}

.student {
  background-color: #d7a84e;
  color: white;
}

.student:hover {
  background-color: #c29843;
}

.student-outline {
  border: 2px solid #d7a84e;
  color: #d7a84e;
}

.student-outline:hover {
  background-color: #d7a84e;
  color: white;
}

@media (max-width: 768px) {
  .auth-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .auth-column {
    width: 100%;
  }
}
</style>
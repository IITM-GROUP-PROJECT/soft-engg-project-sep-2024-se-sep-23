<template>
  <div class="login-container">
    <div class="login-card">
      <img src="/iitm.png" alt="IITM Logo" class="login-logo" />
      <h2>Student Login</h2>
      <p class="welcome-text">Welcome back, Student!</p>
      
      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="email">Email</label>
          <div class="input-group">
            <i class="fas fa-envelope"></i>
            <input 
              id="email"
              type="email" 
              v-model="email" 
              class="form-control" 
              placeholder="Enter your email"
              required
            >
          </div>
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <div class="input-group">
            <i class="fas fa-lock"></i>
            <input 
              id="password"
              type="password" 
              v-model="password" 
              class="form-control" 
              placeholder="Enter your password"
              required
            >
          </div>
        </div>

        <button type="submit" class="login-button student-theme">
          <span>Login</span>
          <i class="fas fa-arrow-right"></i>
        </button>

        <div class="links">
          <router-link to="/student-signup">New Student? Register here</router-link>
        </div>
      </form>
    </div>
  </div>
</template>


<script>
export default {
  name: 'StudentLogin',
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    login() {
      fetch('http://127.0.0.1:5000/api/student_login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: this.email,
          password: this.password
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.access_token) {
          localStorage.setItem('token', data.access_token);
          alert('Login successful');
          this.$router.push('/student_dashboard');
        } else {
          alert('Login failed');
        }
      });
    }
  }
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(121, 25, 18, 0.1) 0%, rgba(215, 168, 78, 0.1) 100%);
  padding: 2rem;
}

.login-card {
  background: white;
  padding: 2.5rem;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 450px;
  text-align: center;
}

.login-logo {
  height: 80px;
  margin-bottom: 1.5rem;
}

h2 {
  color: #791912;
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.welcome-text {
  color: #666;
  margin-bottom: 2rem;
}

.login-form {
  text-align: left;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

.input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.input-group i {
  position: absolute;
  left: 1rem;
  color: #d7a84e;
}

.form-control {
  width: 100%;
  padding: 0.8rem 1rem 0.8rem 2.5rem;
  border: 2px solid #eee;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: #d7a84e;
  outline: none;
  box-shadow: 0 0 0 3px rgba(215, 168, 78, 0.1);
}

.login-button {
  width: 100%;
  padding: 1rem;
  background: #d7a84e;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.login-button:hover {
  background: #c29843;
  transform: translateY(-2px);
}

.login-button i {
  transition: transform 0.3s ease;
}

.login-button:hover i {
  transform: translateX(5px);
}

.links {
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  text-align: center;
}

.links a {
  color: #d7a84e;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}

.links a:hover {
  color: #791912;
}

@media (max-width: 480px) {
  .login-card {
    padding: 2rem;
  }

  h2 {
    font-size: 1.5rem;
  }
}
</style>
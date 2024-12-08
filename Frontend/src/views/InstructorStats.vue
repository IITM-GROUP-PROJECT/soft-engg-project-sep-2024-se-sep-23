<template>
  <div>
    <nav class="navbar">
      <div class="navbar-content">
        <div class="navbar-brand">
          <img src="/iitm.png" alt="IITM Logo" class="navbar-logo" />
          <span>Project Overview</span>
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
  <div class="dashboard">
    <br>
    <h2>Instructor Dashboard</h2>
    <div class="overview">
      <div class="overview-item">
        <p><i class="fas fa-graduation-cap"></i> Total Courses: {{ data.overview.total_courses }}</p>
      </div>
      <div class="overview-item">
        <p><i class="fas fa-tasks"></i> Total Projects: {{ data.overview.total_projects }}</p>
      </div>
      <div class="overview-item">
        <p><i class="fas fa-users"></i> Total Students: {{ data.overview.total_students }}</p>
      </div>
    </div>

    <div v-for="course in data.courses" :key="course.course_id" class="course">
      <div class="course-header" @click="toggleCourse(course.course_id)">
        <h3>{{ course.name }}</h3>
        <i class="material-icons">
          {{ course.showDetails ? 'expand_less' : 'expand_more' }}
        </i>
      </div>
      <div v-if="course.showDetails" class="projects">
        <div v-for="project in course.projects" :key="project.project_id" class="project">
          <div class="project-header" @click="toggleProject(project.project_id)">
            <h4>{{ project.title }}</h4>
            <i class="material-icons">
              {{ project.showDetails ? 'expand_less' : 'expand_more' }}
            </i>
          </div>
          <div v-if="project.showDetails" class="stats">
            <div class="charts-container">
              <div class="chart">
                <h4>Milestone Timeline</h4>
                <TimelineChart :milestoneStats="project.milestone_stats" />
              </div>
              <div class="chart">
                <h4>Milestone Progress</h4>
                <BarChart :dataset="getMilestoneDataset(project.milestone_stats)" :options="chartOptions" />
              </div>
            </div>
            <br>
            <h4>Students</h4>
            <table>
              <thead>
                <tr>
                  <th>Email</th>
                  <th>GitHub Repo</th>
                  <th>Completed Milestones</th>
                  <th>Pending Milestones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="student in project.students" :key="student.student_email">
                  <td>{{ student.student_email }}</td>
                  <td>
                    <a :href="student.github_repo_url" target="_blank">{{ student.github_repo_url }}</a>
                  </td>
                  <td>{{ student.completed_milestones }}</td>
                  <td>{{ student.pending_milestones }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>  
</template>

<script>
import BarChart from "@/components/charts/BarChart.vue";
import TimelineChart from "@/components/charts/TimeLineChart.vue"; // Assuming you have a TimelineChart component

export default {
  components: {
    BarChart,
    TimelineChart,
  },
  data() {
    return {
      data: {
        instructorId: null,
        overview: {
          total_courses: 0,
          total_projects: 0,
          total_students: 0,
        },
        courses: [],
      },
      chartOptions: {
        responsive: true,
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: "Milestone Progress",
          },
        },
        scales: {
          x: {
            stacked: true,
          },
          y: {
            stacked: true,
          },
        },
      },
    };
  },
  created() {
    this.fetchData();
    this.instructorId = this.$route.params.instructorId;
  },
  methods: {
    fetchData() {
    // const instructorId = localStorage.getItem('instructor_id'); // Assuming instructor ID is stored in localStorage
    const instructorId = this.$route.params.instructorId; // Get instructor ID from the route params
    if (!instructorId) {
      console.error("Instructor ID not found");
      return;
    }

    fetch(`http://localhost:5000/api/instructor_stats/${instructorId}`) // Pass the ID in the URL
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch instructor stats");
        }
        return response.json();
      })
      .then((responseData) => {
        // Add showDetails properties for toggle functionality
        responseData.courses.forEach((course) => {
          course.showDetails = false;
          course.projects.forEach((project) => {
            project.showDetails = false;
          });
        });
        this.data = responseData;
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  },
    toggleCourse(courseId) {
      const course = this.data.courses.find((c) => c.course_id === courseId);
      course.showDetails = !course.showDetails;
    },
    toggleProject(projectId) {
      const project = this.data.courses
        .flatMap((c) => c.projects)
        .find((p) => p.project_id === projectId);
      project.showDetails = !project.showDetails;
    },
    getMilestoneDataset(milestoneStats) {
      const labels = Object.keys(milestoneStats);
      const completedData = labels.map((label) => milestoneStats[label].completed);
      const pendingData = labels.map((label) => milestoneStats[label].pending);
      return {
        labels,
        datasets: [
          {
            label: "Completed",
            data: completedData,
            backgroundColor: "#4caf50",
          },
          {
            label: "Pending",
            data: pendingData,
            backgroundColor: "#ff9800",
          },
        ],
      };
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
    },
    goBack() {
      this.$router.push('/instructor_dashboard');
    },
  },
};
</script>

<style scoped>
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

.back-btn:hover i {
  color: white; /* Ensure the icon color changes on hover */
}

.logout-btn {
  background-color: #dc3545;
  border: none;
  color: white;
}

.logout-btn:hover {
  background-color: #c82333;
}

.logout-btn i {
  color: white; /* Ensure the icon color changes on hover */
} 


.dashboard {
  max-width: 1400px;
  margin: 6rem auto 2rem;
  padding: 0 2rem;
  min-height: 100vh;
  font-family: "Roboto", sans-serif;
  /* margin: 20px;
  padding: 20px; */
  background-color: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.overview {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.overview-item {
  display: flex;
  align-items: center;
  font-size: 27px;
}

.fas {
  color: #8a1c14;
}

.course,
.project {
  margin: 20px 0;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.course-header,
.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.course-header .material-icons,
.project-header .material-icons {
  color: #8a1c14; /* Set icon color to #8a1c14 */
  font-size: 34px; /* Increase icon size */
}

.charts-container {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}

.chart {
  width: 48%;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

table th,
table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: center;
}

table th {
  background-color: #f4f4f4;
  font-weight: 600;
}

table tr:nth-child(even) {
  background-color: #f9f9f9;
}

table tr:hover {
  background-color: #f1f1f1;
}

a {
  color: #1e88e5;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
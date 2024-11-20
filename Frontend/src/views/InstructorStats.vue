<template>
  <v-container fluid>
    <v-row>
      <!-- Welcome Banner -->
      <v-col cols="12">
        <v-card class="pa-4">
          <h2 class="text-h5">Welcome, Instructor!</h2>
          <p>Here’s an overview of your projects, students, and milestones.</p>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <!-- Projects Count Card -->
      <v-col cols="12" md="4">
        <v-card outlined class="pa-4 text-center">
          <v-icon large color="blue">mdi-folder</v-icon>
          <h3>{{ stats.projectsCount }}</h3>
          <p>Projects</p>
        </v-card>
      </v-col>

      <!-- Students Count Card -->
      <v-col cols="12" md="4">
        <v-card outlined class="pa-4 text-center">
          <v-icon large color="green">mdi-account-group</v-icon>
          <h3>{{ stats.studentsCount }}</h3>
          <p>Students</p>
        </v-card>
      </v-col>

      <!-- Milestones Count Card -->
      <v-col cols="12" md="4">
        <v-card outlined class="pa-4 text-center">
          <v-icon large color="orange">mdi-flag-checkered</v-icon>
          <h3>{{ stats.milestonesCount }}</h3>
          <p>Milestones</p>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <!-- Projects Progress Chart -->
      <v-col cols="12" md="6">
        <v-card outlined>
          <v-card-title>Project Progress</v-card-title>
          <line-chart :data="chartData" :options="chartOptions" />
        </v-card>
      </v-col>

      <!-- Milestones Status Chart -->
      <v-col cols="12" md="6">
        <v-card outlined>
          <v-card-title>Milestones Status</v-card-title>
          <pie-chart :data="milestonesChartData" :options="chartOptions" />
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <!-- Students Table -->
      <v-col cols="12">
        <v-card outlined>
          <v-card-title>Students Overview</v-card-title>
          <v-data-table
            :headers="tableHeaders"
            :items="students"
            class="elevation-1"
          ></v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { Line, Pie } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  ArcElement
} from 'chart.js';

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  ArcElement
);

export default {
  components: {
    LineChart: Line,
    PieChart: Pie
  },
  data() {
    return {
      stats: {
        projectsCount: 0,
        studentsCount: 0,
        milestonesCount: 0
      },
      chartData: {
        labels: ['Project 1', 'Project 2', 'Project 3'],
        datasets: [
          {
            label: 'Progress (%)',
            backgroundColor: '#3f51b5',
            borderColor: '#3f51b5',
            data: [80, 60, 40]
          }
        ]
      },
      milestonesChartData: {
        labels: ['Completed', 'Pending'],
        datasets: [
          {
            data: [60, 40],
            backgroundColor: ['#4caf50', '#f44336']
          }
        ]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false
      },
      tableHeaders: [
        { text: 'Student ID', value: 'id' },
        { text: 'Email', value: 'email' },
        { text: 'GitHub Repo', value: 'github_repo_url' },
        { text: 'Status', value: 'status' }
      ],
      students: []
    };
  },
  created() {
    this.fetchStats();
  },
  methods: {
    async fetchStats() {
      try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        // Compute stats
        this.stats.projectsCount = data.length;
        this.stats.studentsCount = data.reduce(
          (acc, project) => acc + project.students.length,
          0
        );
        this.stats.milestonesCount = data.reduce(
          (acc, project) => acc + project.milestones.length,
          0
        );

        // Extract students
        this.students = data.flatMap((project) =>
          project.students.map((student) => ({
            id: student.id,
            email: student.email,
            github_repo_url: student.github_repo_url,
            status: student.status
          }))
        );
      } catch (error) {
        console.error('Failed to fetch stats:', error);
      }
    }
  }
};
</script>

<style scoped>
v-container {
  padding: 20px;
}
.text-center {
  text-align: center;
}
</style>

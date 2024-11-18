<template>
  <div class="card">
    <div class="card-header">
      <h3>Commit History</h3>
    </div>
    <div class="card-body">
      <div v-if="loading" class="text-center p-4">
        <p>Loading chart...</p>
      </div>

      <div v-if="error" class="alert alert-danger">
        {{ error }}
      </div>

      <div v-if="!loading && !error" class="chart-container">
        <canvas ref="chartCanvas" id="commitChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart } from 'chart.js/auto';

export default {
  name: 'GitHubCommitHistory',
  
  props: {
    userId: {
      type: String,
      required: true
    }
  },

  data() {
    return {
      loading: false,
      error: null,
      chart: null
    };
  },

  methods: {
 
    async loadChartData() {
      this.error = null;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/get-commit-data?userId=${this.userId}`,{
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Failed to load commit data');
        }

        const commitData = await response.json();
        
        if (commitData.length !== 0) {
          const dates = commitData.map(data => new Date(data.date).toLocaleDateString());
          const commits = commitData.map(data => data.commits);
          this.renderChart(dates, commits);
        } else {
          this.error = "No Commit History Found. Please Re-sync Commits.";
        }

      } catch (err) {
        this.error = err.message;
        console.error('Error loading chart data:', err);
      } finally {
        this.loading = false;
      }
    },

   
    renderChart(labels, data) {
      const canvas = this.$refs.chartCanvas;
      if (!canvas) {
        console.error('Canvas element not found');
        return;
      }

      const ctx = canvas.getContext('2d');
      if (!ctx) {
        console.error('Could not get canvas context');
        return;
      }

      if (this.chart) {
        this.chart.destroy();
      }

      try {
        this.chart = new Chart(ctx, {
          type: 'line',
          data: {
            labels,
            datasets: [{
              label: 'Number of Commits',
              data,
              borderColor: '#2563eb',
              backgroundColor: 'rgba(37, 99, 235, 0.1)',
              borderWidth: 2,
              tension: 0.1,
              fill: true
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: true,
                position: 'top'
              },
              tooltip: {
                mode: 'index',
                intersect: false,
                callbacks: {
                  label: function(context) {
                    return `${context.parsed.y} commits`;
                  }
                }
              }
            },
            scales: {
              x: {
                display: true,
                title: {
                  display: true,
                  text: 'Date'
                }
              },
              y: {
                display: true,
                title: {
                  display: true,
                  text: 'Number of Commits'
                },
                beginAtZero: true,
                ticks: {
                  stepSize: 1
                }
              }
            }
          }
        });
      } catch (err) {
        console.error('Error creating chart:', err);
        this.error = 'Failed to create chart';
      }
    }
  },

  mounted() {
    this.loadChartData();
  },

  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy();
    }
  }
};
</script>

<style scoped>
.card {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.card-header {
  padding: 1rem;
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.card-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.card-body {
  padding: 1rem;
}

.chart-container {
  height: 400px;
  position: relative;
}

.alert-danger {
  color: #dc2626;
  background-color: #fee2e2;
  padding: 1rem;
  border-radius: 0.375rem;
  margin-bottom: 1rem;
}

.text-center {
  text-align: center;
}
</style>

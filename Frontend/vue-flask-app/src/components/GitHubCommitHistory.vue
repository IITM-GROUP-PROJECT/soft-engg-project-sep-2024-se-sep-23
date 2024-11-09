<template>
  <div class="card">
    <div class="card-header">
      <h3>Commit History</h3>
    </div>
    <div class="card-body">
      <!-- Loading State -->
      <div v-if="loading" class="text-center p-4">
        <p>Loading commit history...</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="alert alert-danger">
        {{ error }}
      </div>

      <!-- Chart Container -->
      <div v-if="!loading && !error" class="chart-container">
        <canvas ref="chartCanvas" id="commitChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart } from 'chart.js/auto'

export default {
  name: 'GitHubCommitHistory',
  
  props: {
    repoUrl: {
      type: String,
      required: true
    }
  },

  data() {
    return {
      loading: true,
      error: null,
      chart: null,
      commitData: []
    }
  },

  methods: {
    async fetchCommitData() {
      if (!this.repoUrl) {
        this.error = 'No repository URL provided'
        this.loading = false
        return
      }

      try {
        const urlParts = this.repoUrl.split('/')
        const owner = urlParts[urlParts.length - 2]
        const repo = urlParts[urlParts.length - 1]

        const response = await fetch(`https://api.github.com/repos/${owner}/${repo}/commits`, {
        headers: {
            'Authorization': 'Bearer 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', // Replace 'abcd' with your actual GitHub token
            'Accept': 'application/vnd.github.v3+json'
        }
        });  
        console.log(response)      
        if (!response.ok) {
          throw new Error('Failed to fetch commit data')
        }

        const commits = await response.json()

        const commitsByDate = commits.reduce((acc, commit) => {
          const date = commit.commit.author.date.split('T')[0]
          acc[date] = (acc[date] || 0) + 1
          return acc
        }, {})

        this.commitData = Object.entries(commitsByDate)
          .map(([date, count]) => ({
            date,
            commits: count
          }))
          .sort((a, b) => new Date(a.date) - new Date(b.date))

        this.error = null
        this.$nextTick(() => {
          this.renderChart()
        })
      } catch (err) {
        this.error = 'Failed to load commit history. Please check the repository URL and try again.'
        console.error('Error fetching commit data:', err)
      } finally {
        this.loading = false
      }
    },

    renderChart() {
      const canvas = this.$refs.chartCanvas
      if (!canvas) {
        console.error('Canvas element not found')
        return
      }

      const ctx = canvas.getContext('2d')
      if (!ctx) {
        console.error('Could not get canvas context')
        return
      }
      
      if (this.chart) {
        this.chart.destroy()
      }

      try {
        this.chart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: this.commitData.map(d => new Date(d.date).toLocaleDateString()),
            datasets: [{
              label: 'Number of Commits',
              data: this.commitData.map(d => d.commits),
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
                    return `${context.parsed.y} commits`
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
        })
      } catch (err) {
        console.error('Error creating chart:', err)
        this.error = 'Failed to create chart'
      }
    }
  },

  mounted() {
    if (typeof Chart === 'undefined') {
      this.error = 'Chart.js library not found. Please ensure it is properly loaded.'
      this.loading = false
      return
    }
    this.fetchCommitData()
  },

  watch: {
    repoUrl: {
      handler() {
        this.loading = true
        this.fetchCommitData()
      }
    }
  },

  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy()
    }
  }
}
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
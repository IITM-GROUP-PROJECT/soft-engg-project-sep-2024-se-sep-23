<template>
  <div class="bar-chart-container">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

export default defineComponent({
  name: "BarChart",
  components: {
    Bar,
  },
  props: {
    labels: {
      type: Array,
      required: true,
    },
    dataset: {
      type: Object,
      required: true,
      validator(value) {
        return Array.isArray(value.datasets) && value.datasets.length > 0;
      },
    },
    options: {
      type: Object,
      default: () => ({}),
    },
  },
  computed: {
  chartData() {
    console.log("Dataset:", this.dataset.datasets);
    return {
      labels: this.dataset.labels, // Use labels directly from the dataset
      datasets: this.dataset.datasets,
    };
  },
  chartOptions() {
    return {
      responsive: true,
      indexAxis: "y", // Horizontal bars
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
          ticks: {
            beginAtZero: true,
            callback: function (value) {
              if (Number.isInteger(value)) {
                return value;
              }
              return null; // Skip non-integer values
            },
          },
        },
        y: {
          type: "category", // Category scale for Y-axis
          stacked: true,
        },
      },
      ...this.options,
    };
  },
},

});
</script>




<style scoped>
.bar-chart-container {
  max-width: 1000px;
  max-height: 1500px ;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
  transition: box-shadow 0.3s ease;
}

.bar-chart-container:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.chart-title {
  font-family: "Roboto", sans-serif;
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 16px;
  text-align: center;
}

canvas {
  max-width: 100%;
  height: 100%;
  display: block;
}
</style>

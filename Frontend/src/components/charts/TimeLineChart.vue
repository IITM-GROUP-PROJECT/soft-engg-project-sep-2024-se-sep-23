


<template>
  <div class="timeline-chart-container">
    <h3>Milestone Timeline</h3>
    <apexchart type="rangeBar" :options="chartOptions" :series="chartSeries" />
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts";
import { defineComponent } from "vue";

export default defineComponent({
  name: "TimelineChart",
  components: {
    apexchart: VueApexCharts,
  },
  props: {
    milestoneStats: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      chartOptions: {
        chart: {
          height: 350,
          type: "rangeBar",
        },
        title: {
          text: "Milestone Deadlines",
          align: "center",
        },
        xaxis: {
          type: "datetime",
        },
        yaxis: {
          title: {
            text: "",
          },
        },
        plotOptions: {
          bar: {
            horizontal: true,
          },
        },
      },
      chartSeries: [],
    };
  },
  watch: {
    milestoneStats: {
      handler() {
        this.updateChartSeries();
      },
      immediate: true,
      deep: true,
    },
  },
  methods: {
    getStartOfWeek(date) {
      const startOfWeek = new Date(date);
      const day = startOfWeek.getDay();
      const diff = day; // Subtract day value to get Sunday
      startOfWeek.setDate(startOfWeek.getDate() - diff);
      startOfWeek.setHours(0, 0, 0, 0);
      return startOfWeek;
    },
    updateChartSeries() {
      const milestones = Object.keys(this.milestoneStats);
      const formatted = [];
      let lastEndTime = null;

      milestones.forEach((milestone, index) => {
        const milestoneData = this.milestoneStats[milestone];
        const deadline = new Date(milestoneData.deadline);
        console.log("Deadline:", deadline);
        let startTime = index === 0 ? this.getStartOfWeek(deadline) : new Date(lastEndTime);

        if (startTime > deadline) {
          startTime = new Date(lastEndTime);
        }

        formatted.push({
          x: milestone,
          y: [startTime.getTime(), deadline.getTime()],
        });

        lastEndTime = deadline.getTime();
      });

      this.chartSeries = [{ data: formatted }];
    },
  },
});
</script>






<!-- Dummy Data -->

<!-- <template>
  <div class="timeline-chart-container">
    <h3>Milestone Timeline</h3>
    <apexchart type="rangeBar" :options="chartOptions" :series="chartSeries" />
  </div>
</template> -->

<!-- <script>
import VueApexCharts from "vue-apexcharts";
import { defineComponent } from "vue";

export default defineComponent({
  name: "TimelineChart",
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      milestoneStats: {}, // Placeholder for milestones
      chartOptions: {
        chart: {
          height: 350,
          type: "rangeBar", // RangeBar chart type
        },
        title: {
          text: "Milestone Deadlines",
          align: "center",
        },
        xaxis: {
          type: "datetime", // X-axis shows date range
        },
        yaxis: {
          title: {
            text: "Milestones",
          },
        },
        plotOptions: {
          bar: {
            horizontal: true, // Horizontal bars for range
          },
        },
      },
      chartSeries: [], // Holds the formatted chart data
    };
  },
  computed: {
    formattedData() {
      const milestones = Object.keys(this.milestoneStats);
      const formatted = [];
      let lastEndTime = null;

      milestones.forEach((milestone, index) => {
        const milestoneData = this.milestoneStats[milestone];
        const deadline = new Date(milestoneData.deadline);

        // Determine start time: Start of the week for the first milestone or last end time
        let startTime = index === 0 ? this.getStartOfWeek(deadline) : new Date(lastEndTime);

        // Ensure start time doesn't exceed the deadline
        if (startTime > deadline) {
          startTime = new Date(lastEndTime);
        }

        // Add the formatted data
        formatted.push({
          x: milestone, // Milestone title (y-axis)
          y: [startTime.getTime(), deadline.getTime()], // Start and end timestamps (x-axis)
        });

        // Update lastEndTime
        lastEndTime = deadline.getTime();
      });

      return formatted;
    },
  },
  methods: {
    getStartOfWeek(date) {
      const startOfWeek = new Date(date);
      const day = startOfWeek.getDay();
      const diff = day; // Subtract day value to get Sunday
      startOfWeek.setDate(startOfWeek.getDate() - diff);
      startOfWeek.setHours(0, 0, 0, 0); // Reset time to midnight
      return startOfWeek;
    },
  },
  mounted() {
    // Adding dummy data
    this.milestoneStats = {
      "Milestone 1": { deadline: "Wed, 20 Nov 2024 00:00:00 GMT" },
      "Milestone 2": { deadline: "Sat, 23 Nov 2024 00:00:00 GMT" },
      "Milestone 3": { deadline: "Sun, 24 Nov 2024 00:00:00 GMT" },
      "Milestone 4": { deadline: "Wed, 27 Nov 2024 00:00:00 GMT" },
    };

    // Update the chart series with the formatted data
    this.chartSeries = [{ data: this.formattedData }];
  },
});
</script> -->

<style scoped>
.timeline-chart-container {
  max-width: 1000px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
}

h3 {
  font-family: 'Roboto', sans-serif;
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 16px;
  text-align: center;
}

canvas {
  max-width: 100%;
  height: auto;
  display: block;
}
</style>

import Vue from 'vue';
import Router from 'vue-router';
import HomePage from '../views/HomePage.vue';
import InstructorLogin from '../views/InstructorLogin.vue';
import InstructorSignup from '../views/InstructorSignup.vue';

import StudentLogin from '../views/StudentLogin.vue';
import StudentSignup from '../views/StudentSignup.vue';

import StudentDashboard from '../views/StudentDashboard.vue';
import ProjectInfo from '../views/ProjectInfo.vue';

import InstructorDashboard from '../views/InstructorDashboard.vue';
import CreateProject from '../views/CreateProject.vue';

import ProjectDetails from '../views/ProjectDetails.vue';
import EditProject from '../views/EditProject.vue';
import TrackProgress from '../views/TrackProgress.vue';
import InstructorStats from '../views/InstructorStats.vue'


Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/instructor-login',
      name: 'InstructorLogin',
      component: InstructorLogin
    },
    {
      path: '/instructor-signup',
      name: 'InstructorSignup',
      component: InstructorSignup
    },{
      path: '/student-login',
      name: 'StudentLogin',
      component: StudentLogin
    },
    {
      path: '/student-signup',
      name: 'StudentSignup',
      component: StudentSignup
    },
    {
      path: '/student_dashboard',
      name: 'StudentDashboard',
      component: StudentDashboard
    },
    {
      path: '/instructor_dashboard',
      name: 'InstructorDashboard',
      component: InstructorDashboard
    },
    {
      path: '/create_project',
      name: 'CreateProject',
      component: CreateProject
    },
    {
    path: '/myproject/:id',
    name: 'ProjectInfo',
    component: ProjectInfo,
    props: true
  },
  {
    path: '/project/:projectId',
    name: 'ProjectDetails',
    component: ProjectDetails,
    props: true
  },
  {
    path: '/track_progress/:projectId/:studentId',
    name: 'TrackProgress',
    component: TrackProgress,
    props: true
  },
  {
    path: '/edit_project/:projectId',
    name: 'EditProject',
    component: EditProject,
    props: true
  },
  {
    path: '/instructor_stats',
    name: 'InstructorStats',
    component: InstructorStats,
    props: true
  }
  ]
});
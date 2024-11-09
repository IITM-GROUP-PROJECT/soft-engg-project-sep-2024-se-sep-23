import Vue from 'vue';
import Router from 'vue-router';
import HomePage from '../components/HomePage.vue';  // Update the import statement
import InstructorLogin from '../components/InstructorLogin.vue';
import InstructorSignup from '../components/InstructorSignup.vue';

import StudentLogin from '@/components/StudentLogin.vue';
import StudentSignup from '@/components/StudentSignup.vue';

import StudentDashboard from '@/components/StudentDashboard.vue';
import ProjectInfo from '@/components/ProjectInfo.vue';

import InstructorDashboard from '@/components/InstructorDashboard.vue';
import CreateProject from '@/components/CreateProject.vue';

import ProjectDetails from '@/components/ProjectDetails.vue';
import TrackProgress from '@/components/TrackProgress.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HomePage',  // Update the name to match the new component name
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
  }
  ]
});
// import Vue from 'vue';
// import Router from 'vue-router';
// import Home from '../components/HomePage.vue';
// import InstructorLogin from '../components/InstructorLogin.vue';
// import StudentLogin from '../components/StudentLogin.vue';
// import InstructorSignup from '../components/InstructorSignup.vue';
// import StudentSignup from '../components/StudentSignup.vue';
// import StudentDashboard from '../components/StudentDashboard.vue';
// import InstructorDashboard from '../components/InstructorDashboard.vue';
// import CreateProject from '../components/CreateProject.vue';
// import ProjectInfo from '../components/ProjectInfo.vue';
// import ProjectDetails from '../components/ProjectDetails.vue';
// import TrackProgress from '../components/TrackProgress.vue';

// Vue.use(Router);

// const routes = [
//   {
//     path: '/',
//     name: 'Home',
//     component: Home
//   },
//   {
//     path: '/instructor_login',
//     name: 'InstructorLogin',
//     component: InstructorLogin
//   },
//   {
//     path: '/student_login',
//     name: 'StudentLogin',
//     component: StudentLogin
//   },
//   {
//     path: '/instructor_signup',
//     name: 'InstructorSignup',
//     component: InstructorSignup
//   },
//   {
//     path: '/student_signup',
//     name: 'StudentSignup',
//     component: StudentSignup
//   },
//   {
//     path: '/student_dashboard',
//     name: 'StudentDashboard',
//     component: StudentDashboard
//   },
//   {
//     path: '/instructor_dashboard',
//     name: 'InstructorDashboard',
//     component: InstructorDashboard
//   },
//   {
//     path: '/create_project',
//     name: 'CreateProject',
//     component: CreateProject
//   },
//   {
//     path: '/myproject/:id',
//     name: 'ProjectInfo',
//     component: ProjectInfo,
//     props: true
//   },
//   {
//     path: '/project/:projectId',
//     name: 'ProjectDetails',
//     component: ProjectDetails,
//     props: true
//   },
//   {
//     path: '/track_progress/:projectId/:studentId',
//     name: 'TrackProgress',
//     component: TrackProgress,
//     props: true
//   }
// ];

// export default new Router({
//   routes
// });
import Vue from 'vue';
import Router from 'vue-router';
import HomePage from '../components/HomePage.vue';
import InstructorLogin from '../components/InstructorLogin.vue';
import InstructorSignup from '../components/InstructorSignup.vue';

import StudentLogin from '@/components/StudentLogin.vue';
import StudentSignup from '@/components/StudentSignup.vue';

import StudentDashboard from '@/components/StudentDashboard.vue';
import ProjectInfo from '@/components/ProjectInfo.vue';

import InstructorDashboard from '@/components/InstructorDashboard.vue';
import CreateProject from '@/components/CreateProject.vue';

import ProjectDetails from '@/components/ProjectDetails.vue';
import EditProject from '@/components/EditProject.vue';
import TrackProgress from '@/components/TrackProgress.vue';


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
      path: '/edit_project/:projectId',
      name: 'EditProject',
      component: EditProject,
      props: true
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
  }
  ]
});
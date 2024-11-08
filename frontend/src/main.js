import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)


app.config.globalProperties.$apiRequest = async function({ api, method = 'GET', body = null }) {
  const token = localStorage.getItem('app_token')

  if (!token)
  {
    console.error('No token found in localStorage.')
    return
  }

  try {
    const url = `http://localhost:5000/${api}` // Adjust this based on your Flask server setup

    const headers = {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }

    const options =
    {
      method: method,
      headers: headers,
      body: body ? JSON.stringify(body) : null
    }


    const response = await fetch(url, options)


    if (!response.ok)
    {
      throw new Error(`HTTP error! Status: ${response.status}`)
    }

    const data = await response.json()

    return data
  }
   catch (error)
   {
       console.error('Error making API request:', error)
      return { error: 'Failed to make API request' }
  }
}

app.mount('#app')
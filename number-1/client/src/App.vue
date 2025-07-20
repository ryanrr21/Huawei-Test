<template>
  <div id="app">
    <header>
      <h1>Data Management System</h1>
    </header>

    <main>
      <section id="data">
        <h2>Data Management</h2>
        
        <!-- Form Section -->
        <div class="form-section">
          <h3>Submit New Data</h3>
          <form @submit.prevent="submitForm">
            <div class="form-group">
              <label for="name">Name:</label>
              <input type="text" id="name" v-model="formData.name" required>
            </div>
            
            <div class="form-group">
              <label for="email">Email:</label>
              <input type="email" id="email" v-model="formData.email" required>
            </div>
            
            <div class="form-group">
              <label for="phone">Phone:</label>
              <input type="tel" id="phone" v-model="formData.phone">
            </div>
            
            <div class="form-group">
              <label for="message">Message:</label>
              <textarea id="message" v-model="formData.message" required></textarea>
            </div>
            
            <button type="submit" :disabled="loading">Submit Data</button>
          </form>
          
          <div v-if="message" class="message">
            {{ message }}
          </div>
        </div>

        <!-- Data Table Section -->
        <div class="table-section">
          <h3>Stored Data</h3>
          <button @click="loadData" class="refresh-btn" :disabled="loading">Refresh Data</button>
          
          <div v-if="loading" class="loading">Loading data...</div>
          
          <div v-else-if="dataList.length === 0" class="empty-state">
            <p>No data available. Submit some data to see it here.</p>
          </div>
          
          <div v-else class="data-table">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Phone</th>
                  <th>Message</th>
                  <th>Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in dataList" :key="item.id">
                  <td>{{ item.name }}</td>
                  <td>{{ item.email }}</td>
                  <td>{{ item.phone || '-' }}</td>
                  <td>{{ item.message }}</td>
                  <td>{{ formatDate(item.timestamp) }}</td>
                  <td>
                    <button @click="editItem(item)" class="edit-btn">Edit</button>
                    <button @click="deleteItem(item.id)" class="delete-btn">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Edit Modal -->
        <div v-if="showEditModal" class="modal">
          <div class="modal-content">
            <h3>Edit Data</h3>
            <form @submit.prevent="updateItem">
              <div class="form-group">
                <label for="edit-name">Name:</label>
                <input type="text" id="edit-name" v-model="editData.name" required>
              </div>
              
              <div class="form-group">
                <label for="edit-email">Email:</label>
                <input type="email" id="edit-email" v-model="editData.email" required>
              </div>
              
              <div class="form-group">
                <label for="edit-phone">Phone:</label>
                <input type="tel" id="edit-phone" v-model="editData.phone">
              </div>
              
              <div class="form-group">
                <label for="edit-message">Message:</label>
                <textarea id="edit-message" v-model="editData.message" required></textarea>
              </div>
              
              <div class="modal-buttons">
                <button type="submit" :disabled="loading">Update</button>
                <button type="button" @click="closeEditModal">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      formData: {
        name: '',
        email: '',
        phone: '',
        message: ''
      },
      dataList: [],
      editData: {},
      showEditModal: false,
      loading: false,
      message: ''
    }
  },
  methods: {
    async submitForm() {
      try {
        this.loading = true
        const response = await fetch('/api/submit-data', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.formData)
        })

        if (response.ok) {
          const result = await response.json()
          this.message = 'Data submitted successfully!'
          this.loadData() // Refresh the data list
          
          // Reset form
          this.formData = {
            name: '',
            email: '',
            phone: '',
            message: ''
          }
        } else {
          const error = await response.json()
          this.message = `Error: ${error.message}`
        }
      } catch (error) {
        this.message = 'Error submitting data. Please try again.'
        console.error('Error:', error)
      } finally {
        this.loading = false
        setTimeout(() => {
          this.message = ''
        }, 3000)
      }
    },
    
    async loadData() {
      try {
        this.loading = true
        const response = await fetch('/api/get-data')
        
        if (response.ok) {
          const result = await response.json()
          this.dataList = result.data || []
        } else {
          this.message = 'Error loading data'
        }
      } catch (error) {
        this.message = 'Error loading data. Please try again.'
        console.error('Error:', error)
      } finally {
        this.loading = false
      }
    },
    
    editItem(item) {
      this.editData = { ...item }
      this.showEditModal = true
    },
    
    async updateItem() {
      try {
        this.loading = true
        const response = await fetch(`/api/update-data/${this.editData.id}`, {
          method: 'PATCH', // Using PATCH instead of PUT
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: this.editData.name,
            email: this.editData.email,
            phone: this.editData.phone,
            message: this.editData.message
          })
        })

        if (response.ok) {
          const result = await response.json()
          this.message = 'Data updated successfully!'
          this.closeEditModal()
          this.loadData() // Refresh the data list
        } else {
          const error = await response.json()
          this.message = `Error: ${error.message}`
        }
      } catch (error) {
        this.message = 'Error updating data. Please try again.'
        console.error('Error:', error)
      } finally {
        this.loading = false
        setTimeout(() => {
          this.message = ''
        }, 3000)
      }
    },
    
    async deleteItem(id) {
      if (confirm('Are you sure you want to delete this item?')) {
        try {
          this.loading = true
          const response = await fetch(`/api/delete-data/${id}`, {
            method: 'DELETE'
          })

          if (response.ok) {
            this.message = 'Data deleted successfully!'
            this.loadData() // Refresh the data list
          } else {
            const error = await response.json()
            this.message = `Error: ${error.message}`
          }
        } catch (error) {
          this.message = 'Error deleting data. Please try again.'
          console.error('Error:', error)
        } finally {
          this.loading = false
          setTimeout(() => {
            this.message = ''
          }, 3000)
        }
      }
    },
    
    closeEditModal() {
      this.showEditModal = false
      this.editData = {}
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    }
  },
  
  mounted() {
    this.loadData()
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  line-height: 1.6;
  color: #333;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  background: #f4f4f4;
  padding: 1rem;
  text-align: center;
}

header h1 {
  margin-bottom: 1rem;
}

main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

section {
  margin-bottom: 3rem;
}

h2 {
  margin-bottom: 1rem;
  color: #333;
}

h3 {
  margin-bottom: 1rem;
  color: #333;
}

p {
  margin-bottom: 1rem;
}

.form-section, .table-section {
  background: #f9f9f9;
  padding: 2rem;
  border-radius: 5px;
  margin-top: 2rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

input, textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 3px;
  font-size: 1rem;
}

textarea {
  height: 100px;
  resize: vertical;
}

button {
  background: #333;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-size: 1rem;
  margin-right: 0.5rem;
}

button:hover:not(:disabled) {
  background: #555;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.edit-btn {
  background: #007bff;
}

.edit-btn:hover:not(:disabled) {
  background: #0056b3;
}

.delete-btn {
  background: #dc3545;
}

.delete-btn:hover:not(:disabled) {
  background: #c82333;
}

.refresh-btn {
  background: #28a745;
  margin-bottom: 1rem;
}

.refresh-btn:hover:not(:disabled) {
  background: #218838;
}

.message {
  margin-top: 1rem;
  padding: 1rem;
  background: #d4edda;
  border: 1px solid #c3e6cb;
  border-radius: 3px;
  color: #155724;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.data-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

th, td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background: #f8f9fa;
  font-weight: bold;
}

tr:hover {
  background: #f5f5f5;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 5px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-buttons {
  margin-top: 1rem;
  text-align: right;
}

footer {
  background: #333;
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}
</style>

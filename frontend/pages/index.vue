<template>
  <v-row justify="center" align="center">
    <v-col md="6" cols="12">
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title>Add numbers</v-card-title>
            <v-card-text>
              <validation-observer
                ref="add_input"
                v-slot="{ invalid }"
              >
                <v-alert v-if="message">{{ message }}</v-alert>
                <v-alert color="red" v-if="errors"
                         type="error">
                  <div v-for="(data,index) of errors">
                    <p class="ma-0">{{ index }} - <span v-for="(info,adex) in data">{{ info }}</span></p>
                  </div>
                </v-alert>
                <form @submit.prevent="add_inputs">
                  <validation-provider
                    v-slot="{ errors }"
                    name="Number Inputs"
                    rules="required"
                  >
                    <v-text-field
                      v-model="inputs"
                      :error-messages="errors"
                      label="Number Inputs*"
                      required
                      outlined
                      chips
                    ></v-text-field>
                  </validation-provider>
                  <v-btn color="primary" type="submit">Add now</v-btn>
                </form>
              </validation-observer>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12">
          <v-card>
            <v-card-title>Search numbers</v-card-title>
            <v-card-text>
              <validation-observer
                ref="search_input"
                v-slot="{ invalid }"
              >
                <form @submit.prevent="searchData">
                  <p><span v-if="messageSuccess === 1">True</span> <span v-else>False</span></p>
                  <validation-provider
                    v-slot="{ errors }"
                    name="Search data"
                    rules="required"
                  >
                    <v-text-field
                      v-model="search"
                      :error-messages="errors"
                      label="Search data*"
                      required
                      outlined
                      chips
                    ></v-text-field>
                  </validation-provider>
                  <v-btn color="primary" type="submit">Search now</v-btn>
                </form>
              </validation-observer>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-col>
    <v-col md="6" cols="12">
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <v-btn @click="dataFetch" block color="primary" outlined>Fetch whole data of yours</v-btn>
          </v-card-title>
          <v-card-text v-if="Object.keys(all_data).length > 0">
            <pre class="font-weight-black">{{ all_data }}</pre>
          </v-card-text>
        </v-card>
      </v-col>
    </v-col>


  </v-row>
</template>

<script>
import {extend, ValidationObserver, ValidationProvider, setInteractionMode} from 'vee-validate'
import {required} from 'vee-validate/dist/rules'

setInteractionMode('eager')
extend('required', {
  ...required,
  message: '{_field_} can not be empty.'
})
export default {
  middleware: 'auth',
  name: 'IndexPage',
  components: {
    ValidationProvider,
    ValidationObserver
  },
  data() {
    return {
      search: "",
      inputs: "",
      message: '',
      all_data: {},
      messageSuccess: 0,
      errors: ''
    }
  },
  mounted() {
    this.dataFetch()
  },

  methods: {
    dataFetch() {
      this.$axios.get('/api/v1/input/all/', {
        headers: {
          'Authorization': `Token ${this.$cookies.get("access_token")}`
        }
      })
        .then(res => {
          this.all_data = res.data
        })
    },
    async searchData() {
      const isValid = await this.$refs.search_input.validate()
      if (isValid) {
        await this.$axios.get(`/api/v1/search/input/${this.search}/`, {
          headers: {
            'Authorization': `Token ${this.$cookies.get("access_token")}`
          }
        })
          .then(() => {
            this.messageSuccess = 1
          }).catch(() => {
            this.messageSuccess = 0
          })
      }
    },
    async add_inputs() {
      const isValid = await this.$refs.add_input.validate()
      if (isValid) {
        await this.$axios.post('/api/v1/add/input/', {
          inputs: this.inputs
        }, {
          headers: {
            'Authorization': `Token ${this.$cookies.get("access_token")}`
          }
        })
          .then(() => {
            this.message = "Successfully added."
            this.errors = ""
            this.inputs = ""
            this.$refs.add_input.reset()
            this.dataFetch()
          }).catch(err => {
            this.message = ""
            this.errors = err.response.data
          })
      }
    }
  },
}
</script>

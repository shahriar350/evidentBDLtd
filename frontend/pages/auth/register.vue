<template>
  <div>
    <v-card>


      <v-card-title>
        Register
      </v-card-title>

      <v-card-subtitle v-if="errors">
        <v-alert color="red"
                 type="error">
          <div v-for="(data,index) of errors">
            <p class="ma-0">{{ index }} - <span v-for="(info,adex) in data">{{ info }}</span></p>
          </div>
        </v-alert>
      </v-card-subtitle>

      <v-card-text>
        <validation-observer
          ref="register"
          v-slot="{ invalid }"
        >
          <form @submit.prevent="login_now">
            <validation-provider
              v-slot="{ errors }"
              name="Your name"
              rules="required"
            >

              <v-text-field
                v-model="form.name"
                :error-messages="errors"
                label="Your name*"
                required
                outlined
                chips
              ></v-text-field>
            </validation-provider>
            <validation-provider
              v-slot="{ errors }"
              name="Phone number"
              rules="required|phone_number"
            >

              <v-text-field
                v-model="form.phone_number"
                :error-messages="errors"
                label="Phone number*"
                required
                outlined
                chips
              ></v-text-field>
            </validation-provider>
            <validation-provider
              v-slot="{ errors }"
              name="Password"
              rules="required|min:6"
            >
              <v-text-field
                v-model="form.password"
                :error-messages="errors"
                label="Password*"
                type="password"
                required
                outlined
                chips
              ></v-text-field>
            </validation-provider>
            <v-card-actions>
              <v-btn color="primary" type="submit">REGISTER</v-btn>
              <v-spacer></v-spacer>
              <v-btn color="accent" type="button" to="/auth/login" :nuxt="true">Login</v-btn>
            </v-card-actions>
          </form>
        </validation-observer>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import {extend, ValidationObserver, ValidationProvider, setInteractionMode} from 'vee-validate'
import {required, min} from 'vee-validate/dist/rules'

setInteractionMode('eager')
extend('required', {
  ...required,
  message: '{_field_} can not be empty.'
})
extend('min', {
  ...min,
  message: '{_field_} value must be greater than 6 characters.'
})

extend('phone_number', {
  message: 'This phone number is not valid. 11 digits are required', // the error message
  validate: value => {
    return /(^(01)[3-9]\d{8})$/.test(value)
  } // the validation function
})
export default {
  components: {
    ValidationProvider,
    ValidationObserver
  },
  head() {
    return {
      title: 'Register Page'
    }
  },
  data() {
    return {
      errors: "",
      form: {
        phone_number: '',
        name: '',
        password: ''
      }
    }
  },
  methods: {
    async login_now() {
      const isValid = await this.$refs.register.validate()
      if (isValid) {
        await this.$axios.post('/api/auth/register/', this.form)
          .then(res => {
            console.log(res.data)
            this.errors = ""
            window.location.href = "/auth/login"
          }).catch(err => {
            this.errors = err.response.data
          })
      }
    },
  }


}
</script>

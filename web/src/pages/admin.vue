<template>
  <v-app class="background" id="inspire">
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-form>
              <v-card class="elevation-12">
                <v-card-title>
                  <v-container justify-center>
                    <v-layout row justify-center>
                     <v-text>Admin</v-text>
                    </v-layout>
                  </v-container>
                </v-card-title>
                <v-card-text>
                  <v-container>
                    <v-text-field
                      prepend-icon="mdi-account"
                      v-model="login.username"
                      :error-messages="usernameErrors"
                      label="Username"
                      required
                      @input="$v.login.username.$touch();"
                      @blur="$v.login.username.$touch();"
                    ></v-text-field>
                    <v-text-field
                      prepend-icon="mdi-lock"
                      :append-icon="
                        showPassword ? 'mdi-eye' : 'mdi-eye-off'
                      "
                      :type="showPassword ? 'text' : 'password'"
                      name="password"
                      label="Password"
                      v-model="login.password"
                      class="input-group--focused"
                      @click:append="showPassword = !showPassword;"
                      required
                      :error-messages="passwordErrors"
                      @input="$v.login.password.$touch();"
                      @blur="$v.login.password.$touch();"
                    ></v-text-field>
                    <v-layout v-if="loginError" row justify-center>
                      <v-icon color="error" class="margin-rx-10"
                        >warning</v-icon
                      >
                      <strong class="red--text text--lighten-1">
                        Username o password errati
                      </strong>
                    </v-layout>
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-container justify-center>
                    <v-layout row justify-center>
                      <v-btn color="primary" @click="submit">Login</v-btn>
                    </v-layout>
                  </v-container>
                </v-card-actions>
              </v-card>
            </v-form>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>

    <div class="loading-overlay" v-if="loading">
      <v-progress-circular size="40" width="4" color="primary" indeterminate>
      </v-progress-circular>
      <div class="loading-word"><p>Login..</p></div>
    </div>
  </v-app>
</template>

<script>
import '@mdi/js';
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";
import axios from "axios";
import router from '../router'


export default {
  mixins: [validationMixin],
  data: () => ({
    showPassword: false,
    loginError: false,
    loading: false,
    login: {
      username: "",
      password: ""
    }
  }),
  validations: {
    login: {
      username: {
        required
      },
      password: {
        required
      }
    }
  },
  methods: {
    submit() {
      console.log("SUBMIT");
      this.$v.$touch();

      if (!this.$v.$invalid) {
        this.auth();
      }
    },
    auth() {
      //START
      this.loading = true;
      this.loginError = false;
       var jd = {
          "uwiIssuedID": this.login.username,
          "password": this.login.password
          }
      //LOGIN
      axios.post("http://localhost:5000/web/auth/login",jd).then((res) => {
            if("access_token" in res.data){
              let jwt_token = res.data.access_token
              sessionStorage.setItem('token',jwt_token)
              this.loading = false;
              router.push({name: "dashboard", params:{"token":jwt_token}})
            }}).catch(err => {
          console.error(JSON.stringify(err));
          this.loading = false;
        });
    }
  },
  computed: {
    usernameErrors() {
      const errors = [];
      if (!this.$v.login.username.$dirty) return errors;
      !this.$v.login.username.required &&
        errors.push("Username required");
      return errors;
    },
    passwordErrors() {
      const errors = [];
      if (!this.$v.login.password.$dirty) return errors;
      !this.$v.login.password.required &&
        errors.push("Password required");
      return errors;
    }
  }
};
</script>

<style lang="scss">
.v-card {
  border-radius: 50px !important;
}
.margin-rx-10 {
  margin-right: 10px !important;
}
.loading-overlay {
  z-index: 10;
  top: 0;
  left: 0;
  right: 0;
  position: absolute;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  .loading-word {
    position: absolute;
    top: 60%;
    font-weight: 700;
  }
}
</style>

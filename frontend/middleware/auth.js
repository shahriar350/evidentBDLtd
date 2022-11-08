export default async function ({app, redirect, $axios}) {
  const my_cookie = app.$cookies.get('access_token')
  try {
    await $axios.get(`/api/auth/check/token/${my_cookie}/`)
    return true
  } catch (e) {
    return redirect('/auth/login')
  }
  //
}

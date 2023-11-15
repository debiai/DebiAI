<template>
  <div id="legal">
    <button @click="back">Back to DebiAI</button>
    <h2 id="privacy-policy-and-cookies">Privacy Policy and Cookies</h2>
    <p>IRT SYSTEMX does not collect personal data through the use of this website.</p>
    <p>
      If you contact us via email - for example, when you ask for support, send us questions or
      comments, or report a problem - we will collect your name, email address, message, etc. We use
      this data solely in connection with answering the queries we receive.
    </p>
    <h3 id="cookies">Cookies</h3>
    <p>
      In order for IRT SYSTEMX to provide you the best possible experience on this website, we use
      Matomo Analytics to track the usage of our website. Matomo is configured to anonymize your IP
      address before storing it in our database. We do not use any other cookies to track you. We do
      not share any data with third parties. We do not use any data for advertising purposes.
    </p>
    <h3 id="opt-out-of-website-tracking">Opt-out of website tracking</h3>
    <p>
      You can object to the tracking of your browsing on this website. This will protect your
      privacy, but also prevent the owner from learning from your actions and creating a better
      experience for you and other users.
    </p>
    <p>You can opt out of being tracked by our Matomo Analytics instance below:</p>

    <button
      @click="optIn"
      v-if="userHasOptedOut"
    >
      Opt-in to website tracking
    </button>
    <button
      @click="optOut"
      v-else
    >
      Opt-out of website tracking
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userHasOptedOut: false,
    };
  },
  mounted() {
    this.userHasOptedOut = this.$matomo.isUserOptedOut();
  },
  methods: {
    back() {
      this.$router.push("/");
    },
    optIn() {
      this.$matomo.forgetUserOptOut();
      this.userHasOptedOut = this.$matomo.isUserOptedOut();
      if (!this.userHasOptedOut) {
        this.$store.commit("sendMessage", {
          title: "success",
          msg: "You have opted in to website tracking.",
        });
      }
    },
    optOut() {
      this.$matomo.optUserOut();
      this.userHasOptedOut = this.$matomo.isUserOptedOut();
      if (this.userHasOptedOut) {
        this.$store.commit("sendMessage", {
          title: "success",
          msg: "You have opted out of website tracking.",
        });
      }
    },
  },
};
</script>

<style lang="scss" scoped>
#legal {
  padding: 20px 20px;
  text-align: justify;

  max-width: 800px;
  margin: 0 auto;

  h1 {
    font-size: 2.5rem;
    margin-bottom: 2.5rem;
    margin-top: 2.5rem;
  }

  h2 {
    font-size: 2rem;
    margin-top: 2rem;
    margin-bottom: 2rem;
  }
}
</style>

<template>
  <div id="legal">
    <button @click="back">Back to DebiAI</button>

    <h1 id="legal-notice">Legal Notice</h1>

    <b>Publisher</b>: INSTITUT DE RECHERCHE TECHNOLOGIQUE SYSTEMX
    <br />
    <b>Registered office</b>: 2 boulevard Thomas Gobert 921120 PALAISEAU
    <br />
    <b>Phone number</b>: + 33 (0)1 69 08 05 14
    <br />
    <b>Publishing Director</b>: Mr Michel Morvan
    <br />
    <b>Host</b>: OVH.COM 2 rue Kellermann 59100 Roubaix France
    <br />

    <h2 id="intellectual-property">Copyright</h2>

    <p>
      The IRT SystemX and/or its partners are the exclusive owners of all intellectual property
      rights relating to both the structure and the content of the website
      <a :href="url">{{ url }},</a> and this the world over.
    </p>
    <p>
      The elements of this website, <a :href="url">{{ url }},</a> are protected by copyright and may
      not be copied or imitated in whole or in part. Any reproduction is therefore subject to the
      agreement of the author in accordance with Article L.122-4 of the French Code of Intellectual
      Property. Copyright infringement is a punishable offense under Article L.335-2 of the Code of
      Intellectual Property. It is passable of 3 years imprisonment and 300,000 € fine.
    </p>

    <p>
      IRT SystemX undertakes, as much as possible, to provide you with honest information in good
      faith. However, the information on this website is not contractually binding for IRT SystemX
      or the reader of the website.
    </p>
    <p>The following are permitted without express authorization:</p>

    <ul>
      <li>
        Citations which respect the author's right to attribution and integrity by citing their name
        and the source. The citation must be both a short excerpt from the original publication and
        a short insertion into the publication it later appears in. The citation illustrates a
        statement and must not compete with the source publication.
      </li>
      <li>
        Creating a link, provided that it opens a new, separate window of the browser, and that the
        page that the link leads to is not embedded inside other pages of a different site,
        particularly through the use of frames, belonging to the linked site. Using so many
        citations as to constitute a compilation is considered to be a derivative work, and is
        therefore subject to the prior agreement of the author or copyright holder.
      </li>
    </ul>
    <p>In other cases, and in particular:</p>

    <ul>
      <li>If you want to display the logo of IRT SystemX</li>
      <li>
        If the contents of the site <a :href="url">{{ url }}</a> are to be integrated into the
        appearance of your site, particularly through the use of frames
      </li>
      <li>
        If the pages containing the link to the site <a :href="url">{{ url }}</a> are behind a
        paywall
      </li>
    </ul>

    <p>
      You must request authorization from IRT SystemX by writing to:
      <a href="mailto:communication@irt-systemx.fr">communication@irt-systemx.fr </a>
    </p>
    <p>
      In all cases, IRT SystemX reserves the right to request that a citation or link be removed if
      IRT SystemX believes that it violates its editorial policy or could harm its interests.
    </p>

    <h2 id="privacy-policy-and-cookies">Privacy Policy</h2>
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
      url: "https://demo.debiai.fr/",
    };
  },
  mounted() {
    if (!this.$matomo) {
      console.error("Matomo not initialized");
      return;
    }
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

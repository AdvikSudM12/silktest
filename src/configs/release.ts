export const daysGoneForStartSites = Number(process.env.DAYS_GONE_FOR_START_SITES) || 14

export default {
  name: '',
  status: 'new',
  subtitle: '',
  langMeta: '',
  releaseType: '',
  releaseKind: '',
  tracks: [],
  cover: {
    name: '',
    url: ''
  },
  personsAndRoles: [],
  genre: '',
  subgenre: '',
  code: '',
  label: '',
  dateFirstPublication: null,
  dateStartSites: null,
  datePreorder: null,
  dateCopyright: null,
  description: '',
  booklet: {
    name: '',
    url: ''
  },
  video: {
    name: '',
    url: ''
  },
  videoCover: {
    name: '',
    url: ''
  },
  videoPlatforms: [],
  audioPlatforms: [],
  regions: [],
  sitesParameters: {
    appleMusic: {
      dateStart: null,
      allowedAppleMusic: false
    },
    vkMusic: {
      dateStart: null
    },
    spotify: {
      dateStart: null
    },
    tiktok: {
      dateStart: null
    },
    youTube: {
      dateStart: null
    },
    itunes: {
      allowedITunes: false,
      disablePreview: false,
      dateStart: null,
      priceCategoryRelease: { name: '', price: '', currency: '' },
      priceCategoryTrack: { name: '', price: '', currency: '' },
      minimalPriceCategoryTrackAllowed: false,
      minimalPriceCategoryTrack: { name: '', price: '', currency: '' },
      minimalPriceCategoryTrackCountries: []
    }
  },
  messageToModerator: '',
  messageFromModerator: '',
  isVariousArtists: false,
  applyForPromo: false
}

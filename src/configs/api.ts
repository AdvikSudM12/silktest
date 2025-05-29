export default {
  apiUrl: process.env.EMD_API,
  spaceId: process.env.EMD_SPACE,
  headerTokenKeyName: process.env.EMD_HEADER_TOKEN,
  token: process.env.EMD_TOKEN,
  user_id: process.env.EMD_USER_ID,
  tus: {
    enabled: true,
    endpoint: `${process.env.EMD_API}/silk/uploader/chunk/default/s3/`,
    chunkSize: 64 * 1024 * 1024,
    staticUrl: `${process.env.EMD_API}/silk/uploader/chunk/default/file`
  }
}

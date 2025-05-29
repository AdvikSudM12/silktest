// Modules Imports
import axios from 'axios'

// Source code Imports
import apiConfig from 'src/configs/api'

axios.defaults.headers.common.Authorization = `${apiConfig.headerTokenKeyName} ${apiConfig.token}`

export const requestToWebhook = ({
  spaceId = apiConfig.spaceId,
  name,
  params = {},
  body = {},
  method = 'post',
}: {
  spaceId?: string
  name: string
  params?: Record<string, any>
  body?: Record<string, any>
  method?: 'get' | 'post' | 'put' | 'delete'
}) => {
  return new Promise(async (resolve, regect) => {
    try {
      if (method === 'get') {
        const { data } = await axios[method](`${apiConfig.apiUrl}/${spaceId}/webhook/${name}`, {
          params
        })

        resolve(data)
        console.log(`Request ${method.toLocaleUpperCase()} to "${name}" workflow in "${spaceId}" space is success ✅`)

        return 
      }

      const { data } = await axios[method](`${apiConfig.apiUrl}/${spaceId}/webhook/${name}`, body, {
        params
      })

      resolve(data)
      console.log(`Request ${method.toLocaleUpperCase()} to "${name}" workflow in "${spaceId}" space is success ✅`)
    } catch (err) {
      console.error(`Failed request ${method.toLocaleUpperCase()} to "${name}" workflow in "${spaceId}" space ❌`)
      regect(err)
    }
  })
}
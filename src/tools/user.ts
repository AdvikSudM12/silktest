// Modules Imports
import axios from 'axios'

// Source code Imports
import apiConfig from 'src/configs/api'

axios.defaults.headers.common.Authorization = `${apiConfig.headerTokenKeyName} ${apiConfig.token}`

export const getUsers = async ({
  spaceId = apiConfig.spaceId,
  limit = 100,
  page = 0,
  search = ''
}: {
  spaceId?: string
  limit?: number
  page?: number
  search?: string
}) => {
  return new Promise(async (resolve, regect) => {
    try {
      const { data } = await axios.get(`${apiConfig.apiUrl}/${spaceId}/user`, {
        params: {
          limit,
          page,
          search
        }
      })

      console.log(`Get users in "${spaceId}" space is success ✅`)
      resolve(data)
    } catch (err) {
      console.error(`Error get users in "${spaceId}" space ❌`)
      regect(err)
    }
  })
}

export const getUser = async ({
  spaceId = apiConfig.spaceId,
  userId
}: {
  spaceId?: string
  userId: string
}) => {
  return new Promise(async (resolve, regect) => {
    try {
      const { data } = await axios.get(`${apiConfig.apiUrl}/${spaceId}/user/${userId}`)

      console.log(`Get user with ID ${userId} in "${spaceId}" space is success ✅`)
      resolve(data)
    } catch (err) {
      console.error(`Error get user with ID ${userId} in "${spaceId}" space ❌`)
      regect(err)
    }
  })
}

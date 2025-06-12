import dayjs from 'dayjs'
import excelToJson from 'convert-excel-to-json'
import initialReleaseValues from 'src/configs/release'
import { daysGoneForStartSites } from 'src/configs/release'

export const getReleasesDataJson = ({
  sourceFile,
  allCountries = [],
  allAudioPlatformsList = []
}: {
  sourceFile: string
  allCountries?: string[]
  allAudioPlatformsList?: string[]
}) => {
  const { ['Лист1']: singles }: {
    [key: string]: any[]
  } = excelToJson({
    sourceFile,
    header:{ rows: 1 },
    columnToKey: {
      A: 'track',
      B: 'cover',
      C: 'upc',
      D: 'isrc',
      E: 'trackName',
      F: 'genre',
      G: 'subgenre',
      H: 'name',
      I: 'performerReleaseFullname',
      J: 'featReleaseFullname',
      K: 'performerTrackFullname',
      L: 'featTrackFullname',
      M: 'composerFullname',
      N: 'lyricistFullname',
      O: 'explicit',
      P: 'trackLanguage',
      Q: 'label',
      R: 'audioPlatforms',
      S: 'regions',
      T: 'dateFirstPublication',
      U: 'partnerCode'
    },
    sheets: ['Лист1']
  })

  const items = singles.map((item) => {
    const performersRelease: { person: string, role: string }[] = (item.performerReleaseFullname || '')
      ?.split(', ')
      .filter((performerFullName: string) => !!performerFullName)
      .map((performerFullName: string) => ({ person: performerFullName, role: 'performer' }))

    const featRelease: { person: string, role: string }[] = (item.featReleaseFullname || '')
      ?.split(', ')
      .filter((featFullName: string) => !!featFullName)
      .map((featFullName: string) => ({ person: featFullName, role: 'feat.' }))

    const performersTrack: { person: string, role: string[] }[] = (String(item.performerTrackFullname) || '')
      ?.split(', ')
      .filter((performerFullName: string) => !!performerFullName)
      .map((performerFullName: string) => ({ person: performerFullName, role: ['performer'] }))

    const featsTrack: { person: string, role: string[] }[] = (item.featTrackFullname || '')
      ?.split(', ')
      .filter((featFullName: string) => !!featFullName)
      .map((featFullName: string) => ({ person: featFullName, role: ['feat.'] }))

    const authorsTrack: { person: string, role: string[] }[] = (item.composerFullname || '')
      ?.split(', ')
      .filter((composerFullName: string) => !!composerFullName)
      .map((composerFullName: string) => ({ person: composerFullName, role: ['music-author'] }))

    const isNoWords = item.lyricsAuthors?.toLocaleLowerCase() === 'без слов'

    let lyricistsTrack: { person: string, role: string[] }[] = []

    if (!isNoWords) {
      lyricistsTrack = (item.lyricistFullname || '')
        ?.split(', ')
        .filter((lyricistFullName: string) => !!lyricistFullName)
        .map((lyricistFullName: string) => ({ person: lyricistFullName, role: ['lyricist'] }))
    }

    const personsAndRolesTrack: { person: string, role: string[] }[] = [
      ...performersTrack,
      ...featsTrack,
      ...authorsTrack,
      ...lyricistsTrack
    ]

    const formatedPersonsAndRolesTrack: { person: string, role: string[] }[] = []

    personsAndRolesTrack.forEach(({ person, role }) => {
      const index = formatedPersonsAndRolesTrack.findIndex((serarchPerson) => person === serarchPerson.person)

      if (index !== -1) formatedPersonsAndRolesTrack[index].role = [...new Set([...formatedPersonsAndRolesTrack[index].role, ...role])]
      else formatedPersonsAndRolesTrack.push({ person, role })
    })

    const upc = (typeof item.upc === 'number' ? item.upc.toString() : item.upc) || ''
    const isrc = (typeof item.isrc === 'number' ? item.isrc.toString() : item.isrc) || ''

    const getAudioPlatforms = (): string[] => {
      if (item.audioPlatforms === 'All') return allAudioPlatformsList

      return item.audioPlatforms
        ?.split(',')
        .filter((item: string) => !!item)
    }

    const getRegions = (): string[] => {
      if (item.regions === 'All' || item.regions === 'WW') return allCountries

      return item.regions
        ?.split(',')
        .filter((item: string) => !!item)
    }

    const dateFirstPublication = item.dateFirstPublication ? dayjs(item.dateFirstPublication).format('YYYY-MM-DD') : null

    const currentDate = new Date()
    currentDate.setDate(currentDate.getDate() + daysGoneForStartSites)
    const dateStartSites = dayjs(currentDate).format('YYYY-MM-DD')

    const trackLanguage = item.trackLanguage?.toLowerCase() || (isNoWords ? 'no-words' : null)

    const tracks = [{
      name: item.trackName || 'unknown',
      src: item.track,
      subtitle: item.subtitle || '',
      authorRights: 0,
      relatedRights: 100,
      trackVersion: [],
      tiktokStartAt: '00:00.001',
      tiktokEndAt: '',
      personsAndRoles: formatedPersonsAndRolesTrack,
      instantGratification: false,
      timeStartPreview: '',
      dateStartPreview: null,
      code: isrc,
      lyrics: '',
      trackLanguage,
      karaokeFile: {
        name: '',
        url: ''
      },
      syncLyrics: false,
      ringtone: {
        name: '',
        url: ''
      },
      video: {
        name: '',
        url: ''
      },
      order: 0
    }]

    return {
      ...initialReleaseValues,
      name: item.name,
      cover: item.cover,
      genre: item.genre,
      subgenre: item.subgenre,
      dateStartSites,
      dateFirstPublication,
      partnerCode: item.partnerCode,
      code: upc,
      personsAndRoles: [...performersRelease, ...featRelease],
      tracks,
      audioPlatforms: getAudioPlatforms(),
      regions: getRegions(),
      label: item.label
    }
  })

  return items
    .reduce((acc: any[], currentValue) => {
      let existingItem: any

      if (!currentValue.code) existingItem = acc.find(item => item.name === currentValue.name)
      else existingItem = acc.find(item => item.code === currentValue.code)

      if (existingItem) existingItem.tracks = existingItem.tracks.concat(currentValue.tracks)
      else acc.push(currentValue)

      return acc
    }, [])
    .map((item) => {
      return {
        ...item,
        releaseType: item.tracks.length > 5 ? 'album' : 'single',
        releaseKind: (item.tracks.length > 1 && item.tracks.length <= 5) ? 'single-maxi' : undefined
      }
    })
}

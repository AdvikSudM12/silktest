export const countriesOpts = (allOptions: string[]) => ({
  World: allOptions,
  CIS: [
    'RUS',
    'UKR',
    'AZE',
    'ARM',
    'GEO',
    'MDA',
    'KAZ',
    'KGZ',
    'TJK',
    'UZB',
    'TKM',
    'BLR'
  ]
})

export const audioPlatformsOpts = (allOptions: string[]) => ({
  All: allOptions,
  CIS: [
    'Beeline Music UZ',
    'Мотив',
    'Moldcell (РБТ)',
    'МТС Беларусь (музыкальный портал)',
    'hitter',
    'MobiMusic (Казахстан)',
    'Теле2 (РБТ)',
    'Мегафон (РБТ)',
    'РБТ-Партнёрка',
    'МТС (РБТ)',
    'VK Музыка',
    'Яндекс.Музыка',
    'Звук',
    'Yappy',
    'Likee'
  ],
  'All except YouTube, Soundcloud и Beatport': allOptions.filter((item) => (
    item !== 'YouTube Music' &&
    item !== 'YouTube (Sound Recording)' &&
    item !== 'YouTube Copyright' &&
    item !== 'Soundcloud'
  ))
})

export const uniqueArray = (arr: any[], key: string) => {
  return arr.reduce((accumulator, current) => {
    let existing = accumulator.find((item: any) => item[key] === current[key])

    if (!existing) return accumulator.concat(current)
    else return accumulator
  }, [])
}

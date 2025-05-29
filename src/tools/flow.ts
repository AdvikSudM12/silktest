export const tableFlowIterations = (
  callback: (iteration: number) => void,
  {
    initialIteration = 0,
    iterations,
    interval = 500
  }: {
    initialIteration?: number
    iterations: number
    interval?: number
  }
) => {
  return new Promise((resolve, regect) => {
    let iteration = initialIteration

    const onIterate = async () => {
      try {
      if (iterations > iteration) {
        await callback(iteration)

        ++iteration

        setTimeout(onIterate, interval)
      } else {
        console.log('Flow completed ✅')
        resolve(true)
      }
      } catch (err) {
        console.error(`Flow failed on ${iteration} iteration ❌`)
        regect(err)
      }
    }

    onIterate()
  })
}

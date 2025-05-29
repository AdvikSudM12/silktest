class ProgressBarConsole {
  rewriteble: boolean

  constructor() {
    this.rewriteble = false
  }

  start() {
    this.rewriteble = true
  }

  end() {
    process.stdout.write('\n')
    this.rewriteble = false
  }

  write(procentage: number, text: string) {
    const rewriteble = this.rewriteble ? '\r' : '\n'

    const prograsLineList = Array(100).fill('=').map((_item, index) => ++index <= procentage ? '#' : '=')
    const firstSide = prograsLineList.filter((_item, index) => ++index < 50).join('')
    const lastSide = prograsLineList.filter((_item, index) => ++index >= 50).join('')

    const renderProgressBar = `[${firstSide}/ ${text} /${lastSide}]`

    process.stdout.write(`${renderProgressBar}${rewriteble}`)
  }
}

export default ProgressBarConsole

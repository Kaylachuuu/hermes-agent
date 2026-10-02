import { expect, test, vi } from 'vitest'
const handlers = vi.hoisted(() => new Map<string, (...args: any[]) => any>())
vi.mock('electron', () => ({ app: { getVersion: () => 'test', getPath: () => process.env.HOME }, ipcMain: { handle: (name: string, handler: (...args: any[]) => any) => handlers.set(name, handler), on: () => {} } }))
vi.mock('node-pty', () => ({ default: {} }))
vi.mock('./pc-ipc', () => ({ registerPcIpc: () => {} }))
import { registerTerminalIpc } from './terminal-ipc'
test.runIf(process.platform === 'linux')('explicit Bash runs locally without Windows Git Bash configuration', async () => {
  registerTerminalIpc({ pcConnectionScope: () => 'test', isWindows: false, findOnPath: () => null, rememberLog: () => {}, activeSshTerminalTarget: () => null, sshBinary: () => '/usr/bin/ssh', ensureBackend: async () => undefined, getSshConnectionState: () => undefined })
  const result = await handlers.get('hermes:desktop:exec')!({}, { shell: 'bash', command: 'uname -s', cwd: '/tmp' })
  expect(result.success).toBe(true)
  expect(result.output.trim()).toBe('Linux')
  expect(result.shell).toBe('bash')
})


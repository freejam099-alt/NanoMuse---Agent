import type { AppManifest } from '@/os/types/manifest';
import { IcLauncher } from './res/icons';

/**
 * nanoMuse as an app on the simulated phone.
 *
 * The app is a thin shell: it shows the nanoMuse web app (served by `nanomuse serve` on the
 * host) full-screen, and mirrors what the server wants from you — approvals, questions,
 * background results — into the simulator's notification shade.
 */
export const manifest: AppManifest = {
  id: 'nanomuse',
  packageName: 'org.nanomuse.app',
  displayName: 'nanoMuse',
  displayNameEn: 'nanoMuse',
  aliases: ['muse', 'open muse', 'personal agent', 'assistant'],
  version: '0.2.0',
  versionCode: 2,
  type: 'plugin',
  icon: IcLauncher,
  iconBackground: '#ffffff', // the Android app's light tile; the mark keeps its own colours
  iconForeground: '#0a66e4',
  designViewportWidth: 360,
  // the web app's palette (web/src/index.css) and the Android app's action blue (MuseTones)
  theme: {
    colors: {
      primary: '#015CFB',
      primaryDark: '#015CFB',
      onPrimary: '#ffffff',
      accent: '#015CFB',
      background: '#fcfcfc',
      surface: '#ffffff',
      textPrimary: '#111112',
      textSecondary: '#6b6b71',
      border: '#e5e5ea',
      statusBarForeground: 'dark',
      navigationBarForeground: 'dark',
    },
    colorsDark: {
      primary: '#58A6FF',
      primaryDark: '#58A6FF',
      onPrimary: '#000000',
      accent: '#58A6FF',
      background: '#181819',
      surface: '#1c1c1e',
      textPrimary: '#ffffff',
      textSecondary: '#9d9da4',
      border: '#3a3a3c',
      statusBarForeground: 'light',
      navigationBarForeground: 'light',
    },
  },
  // the system splash — the icon on the app's background, as Android's — nothing added
};

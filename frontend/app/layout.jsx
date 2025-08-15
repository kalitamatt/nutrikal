import { Providers } from './providers';
import Link from 'next/link';

export const metadata = {
  title: 'NUTRIKAL',
  description: 'Nutrition cérébrale personnalisée',
};

export default function RootLayout({ children }) {
  return (
    <html lang="fr">
      <body>
        <Providers>
          <header style={{ padding: '12px 20px', borderBottom: '1px solid #eee' }}>
            <nav style={{ display: 'flex', gap: 16 }}>
              <Link href="/">Accueil</Link>
              <Link href="/profile">Profil</Link>
              <Link href="/dashboard">Dashboard</Link>
            </nav>
          </header>
          {children}
        </Providers>
      </body>
    </html>
  );
}

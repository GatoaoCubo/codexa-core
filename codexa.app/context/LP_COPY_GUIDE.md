# Guia de Cópia da LP CODEXA

> **Para**: Próximo dev que vai substituir a LP em outro projeto
> **Origem**: `connect-my-github/`
> **Destino**: Projeto alvo com React + Vite + Tailwind

---

## ARQUIVOS PARA COPIAR

### 1. Página Principal (OBRIGATÓRIO)
```
src/pages/Index.tsx → src/pages/Index.tsx
```
**Tamanho**: ~58KB, 1176 linhas
**Contém**: Todas as seções da LP em um arquivo

---

### 2. Componentes (OBRIGATÓRIO)
```
src/components/MatrixRain.tsx    → src/components/MatrixRain.tsx
src/components/ThemeToggle.tsx   → src/components/ThemeToggle.tsx
src/components/ThemeProvider.tsx → src/components/ThemeProvider.tsx
```

---

### 3. Estilos (OBRIGATÓRIO)
```
src/index.css        → src/index.css
tailwind.config.ts   → tailwind.config.ts
```

---

### 4. Assets Públicos (COPIAR TUDO)
```
public/
├── Agente__Analista_de_Mercado.mp4      (24 MB) - Vídeo Pesquisa Agent
├── Anuncio_Agent.mp4                     (25 MB) - Vídeo Anúncio Agent
├── Photo_Agent__Diretor_de_IA.mp4        (29 MB) - Vídeo Photo Agent
├── demo-video.mp4                        (32 MB) - Vídeo hero
├── grafo-pesquisa.png                    (6.7 MB) - Workflow pesquisa
├── grafo-anuncio.png                     (6 MB) - Workflow anúncio
├── grafo-foto.png                        (6.5 MB) - Workflow foto
├── Market_Research_Automation_Strategic_Plan.pdf  (10 MB)
├── Anuncio_Agent_Marketplace_Copywriter.pdf       (11 MB)
├── Photo_Agent_Seu_Diretor_de_Fotografia_IA.pdf   (10 MB)
├── logo-gato3-animated.gif               (7 MB) - Logo Gato³
├── should-i-stay-or-should-i-go.mp3      (7.5 MB) - Easter egg
├── favicon.ico
├── placeholder.svg
└── robots.txt
```

**Total assets**: ~155 MB

---

### 5. Componentes UI (SE NÃO TIVER shadcn/ui)
```
src/components/ui/button.tsx
src/components/ui/... (todos os arquivos da pasta ui/)
```

---

## DEPENDÊNCIAS (package.json)

Verificar se o projeto destino tem:

```json
{
  "dependencies": {
    "lucide-react": "^0.x.x",
    "class-variance-authority": "^0.x.x",
    "clsx": "^2.x.x",
    "tailwind-merge": "^2.x.x"
  }
}
```

Se não tiver:
```bash
npm install lucide-react class-variance-authority clsx tailwind-merge
```

---

## CHECKLIST DE SUBSTITUIÇÃO

```
[ ] 1. Copiar src/pages/Index.tsx
[ ] 2. Copiar src/components/MatrixRain.tsx
[ ] 3. Copiar src/components/ThemeToggle.tsx
[ ] 4. Copiar src/components/ThemeProvider.tsx
[ ] 5. Copiar/mergear src/index.css
[ ] 6. Copiar/mergear tailwind.config.ts
[ ] 7. Copiar pasta public/ inteira (ou assets específicos)
[ ] 8. Copiar src/components/ui/ (se necessário)
[ ] 9. Verificar dependências no package.json
[ ] 10. npm install
[ ] 11. npm run dev - testar
```

---

## COMANDO RÁPIDO (Git Bash)

Se os dois repos estiverem na mesma pasta:

```bash
# Ajustar SOURCE e DEST conforme seus paths
SOURCE="/c/Users/Dell/Documents/GitHub/connect-my-github"
DEST="/c/Users/Dell/Documents/GitHub/OUTRO-PROJETO"

# Copiar página principal
cp "$SOURCE/src/pages/Index.tsx" "$DEST/src/pages/"

# Copiar componentes
cp "$SOURCE/src/components/MatrixRain.tsx" "$DEST/src/components/"
cp "$SOURCE/src/components/ThemeToggle.tsx" "$DEST/src/components/"
cp "$SOURCE/src/components/ThemeProvider.tsx" "$DEST/src/components/"

# Copiar assets (CUIDADO: vai sobrescrever)
cp -r "$SOURCE/public/"* "$DEST/public/"

# Copiar estilos (CUIDADO: vai sobrescrever)
cp "$SOURCE/src/index.css" "$DEST/src/"
cp "$SOURCE/tailwind.config.ts" "$DEST/"
```

---

## NOTAS

### ThemeProvider
Precisa envolver o App:
```tsx
// src/App.tsx
import { ThemeProvider } from "@/components/ThemeProvider";

function App() {
  return (
    <ThemeProvider>
      {/* routes */}
    </ThemeProvider>
  );
}
```

### Imports do Index.tsx
Verificar se os paths de import batem com a estrutura do projeto destino:
```tsx
import { Button } from "@/components/ui/button";
import MatrixRain from "@/components/MatrixRain";
import { ThemeToggle } from "@/components/ThemeToggle";
```

### CHECKOUT_URL
Linha 12 do Index.tsx - atualizar com URL real:
```tsx
const CHECKOUT_URL = "#checkout"; // TODO: Replace
```

---

**Criado**: 2025-12-01
**Projeto origem**: connect-my-github (CODEXA LP v4.0)

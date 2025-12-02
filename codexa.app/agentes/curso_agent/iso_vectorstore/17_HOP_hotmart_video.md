# HOP: Hotmart Video Upload & Player Configuration

**Version**: 1.0.0
**Type**: Operational HOP
**Agent**: curso_agent
**TAC-7 Compliant**: Yes

---

## TAC-7 STRUCTURE

### T - Title
**Upload Videos to Hotmart Player and Configure DRM Settings**

### A - Audience
- Course creators using Hotmart Club
- Curso agent executing content upload workflow
- Producers migrating from other platforms (YouTube, Vimeo)

### C - Context
**When to use this HOP:**
- After product approval in Hotmart
- After Hotmart Club activation
- Before setting gotejamento (drip) schedules
- When replacing/updating existing lesson videos

**Prerequisites:**
- [ ] Videos exported as MP4 (H.264 codec)
- [ ] Resolution: 1080p or 720p minimum
- [ ] Audio: AAC codec, stereo, 128-256 kbps
- [ ] File size: <5GB per video (for optimal upload)
- [ ] Transcripts ready (.SRT or .VTT files)

### T - Task
**Upload course videos to Hotmart Player, configure DRM protection, enable transcripts, and optimize player settings for maximum completion rates.**

### A - Approach

#### STEP 1: Access Video Library (Biblioteca de Vídeos)

1. Log in to Hotmart panel: https://app-vlc.hotmart.com
2. Navigate to: **Products → [Your Product] → Hotmart Club**
3. In left sidebar, click: **Biblioteca de Vídeos** (Video Library)
4. This is your centralized video storage (all videos here can be reused across modules)

**Pro Tip**: Upload all videos to library first, then embed in lessons. This allows reuse without re-uploading.

---

#### STEP 2: Upload Video to Library

**Method A: Direct Upload (Recommended)**

1. Click **"+ Novo Vídeo"** (New Video)
2. Choose **"Fazer Upload"** (Upload)
3. Select file from computer:
   - Supported formats: MP4, MOV, AVI (MP4 H.264 recommended)
   - Max size: 5GB (larger files may timeout)
   - If file >5GB: compress using Handbrake or Adobe Media Encoder
4. Wait for upload progress bar (time depends on file size and connection)
5. Once uploaded, video enters **processing queue** (5-30 min depending on resolution)
6. You'll receive email notification when processing completes

**Method B: Import from URL (Embed External)**

1. Click **"+ Novo Vídeo"** → **"Incorporar Vídeo"** (Embed Video)
2. Paste URL from:
   - YouTube (public or unlisted)
   - Vimeo (Pro account required for privacy)
   - Other embeddable players
3. ⚠️ **Warning**: External embeds bypass Hotmart DRM (no download protection)
4. Only use if video is non-critical (e.g., free previews, testimonials)

**Method C: Import from Google Drive/Dropbox (Not Recommended)**

1. Hotmart does not support direct import from cloud storage
2. Workaround: Download file locally → Upload to Hotmart
3. For bulk uploads: Use FTP-like tools (not officially supported)

---

#### STEP 3: Configure Video Metadata

After upload completes:

1. **Video Title**: Clear, descriptive (e.g., "Módulo 1 - Aula 3: Configuração do Sistema")
2. **Internal Code** (optional): SKU for tracking (e.g., M1A3-v2)
3. **Description**: 50-100 words summarizing lesson content (used in search)
4. **Tags**: Add keywords (e.g., "setup", "configuração", "primeiros passos")
5. **Thumbnail**:
   - Auto-generated: Hotmart picks frame from video
   - Custom upload: 1280x720px JPG/PNG (branded thumbnail with lesson number)
   - Best practice: Upload custom with text overlay (lesson title + number)
6. **Duration**: Auto-detected (verify it's correct)
7. Click **"Salvar"** (Save)

---

#### STEP 4: Enable DRM & Protection Settings

**Important**: These settings protect your video from unauthorized downloads and sharing.

1. In video settings, scroll to **"Configurações de Segurança"** (Security Settings)
2. **Ativar Proteção DRM**: ✅ Enable (default: ON)
   - This prevents downloads, screen recording detection (partial)
   - Works on Hotmart Player only (not external embeds)
3. **Marca d'água (Watermark)**:
   - Enable: ✅ Yes
   - Type: **Email do aluno** (Student email overlay)
   - Position: Bottom right (least intrusive)
   - Opacity: 50-70% (visible but not distracting)
   - This deters students from sharing video recordings
4. **Bloquear acesso fora do Club**: ✅ Enable
   - Prevents video URL from playing outside Hotmart Club domain
   - Blocks embedding on external sites
5. **Permitir download**: ❌ Disable (unless offering offline access)
   - If enabled: Students can download MP4 (use only for bonuses/PDFs)
6. Click **"Salvar Configurações"**

---

#### STEP 5: Upload Transcript (.SRT/.VTT)

**Why transcripts?**
- Improves accessibility (deaf/hard-of-hearing students)
- Enables search inside Club (students can search lesson by keyword)
- Boosts SEO (Google indexes transcript text)
- Hotmart provides auto-captions, but manual is more accurate

**How to upload:**

1. In video settings, scroll to **"Legenda/Transcrição"** (Captions/Transcript)
2. Click **"+ Adicionar Legenda"**
3. Choose file format:
   - **.SRT** (SubRip Text) - most common
   - **.VTT** (WebVTT) - HTML5 standard
   - **.TXT** (plain text) - not recommended (no timestamps)
4. Select file from computer
5. Choose language: **Português (Brasil)**
6. Set as default: ✅ Yes (auto-display captions)
7. Upload
8. Preview captions in player to verify sync

**Creating .SRT files:**
- **Manual**: Use Subtitle Edit (free software)
- **Auto-generate**: Use YouTube auto-captions, download .SRT, clean up errors
- **AI tools**: Descript, Otter.ai, Fireflies (transcribe audio → export .SRT)

**SRT Format Example:**
```
1
00:00:00,000 --> 00:00:05,000
Bem-vindo ao Módulo 1! Nesta aula, você vai aprender...

2
00:00:05,500 --> 00:00:12,000
Primeiro, vamos configurar o sistema passo a passo.
```

---

#### STEP 6: Configure Player Settings

1. In video settings, find **"Configurações do Player"** (Player Settings)
2. **Barra de Progresso (Seekbar)**:
   - Enable: ✅ Yes (students can skip/rewind)
   - Disable: ❌ No (forces linear watching) - use sparingly
   - Best practice: Enable for lectures, disable for exams/assessments
3. **Velocidade de Reprodução (Playback Speed)**:
   - Enable: ✅ Yes (0.5x, 0.75x, 1x, 1.25x, 1.5x, 2x)
   - Students appreciate flexibility (fast learners use 1.5-2x)
4. **Autoplay Próximo Vídeo (Autoplay Next)**:
   - Enable: ✅ Yes (seamless module flow)
   - Disable: ❌ No (use if exercises required between lessons)
5. **Mostrar Controles (Show Controls)**:
   - Enable: ✅ Yes (volume, fullscreen, quality)
   - Always leave enabled (UX standard)
6. **Qualidade Adaptativa (Adaptive Quality)**:
   - Enable: ✅ Yes (auto-adjusts based on connection speed)
   - Prevents buffering for students with slow internet
7. Click **"Salvar"**

---

#### STEP 7: Add Video to Lesson

Now that video is in library, add it to a lesson:

1. Go to **Hotmart Club → Conteúdo → [Select Module]**
2. Click **"+ Adicionar Aula"** (Add Lesson)
3. Choose **"Vídeo"** as lesson type
4. Select source:
   - **"Da Biblioteca"** (From Library) ← Choose this
   - **"Fazer Upload"** (Direct upload) - skip, already in library
   - **"Incorporar"** (Embed external) - avoid for main content
5. Select your video from library dropdown
6. Set lesson title (e.g., "Aula 3: Configuração do Sistema")
7. Add description (optional, 50-100 words)
8. Attach resources:
   - PDFs, templates, checklists (click **"+ Anexo"**)
   - Max 50MB per attachment
9. Set lesson as:
   - **Obrigatória** (Mandatory) - must complete to unlock next
   - **Opcional** (Optional) - can skip
10. Save lesson

---

#### STEP 8: Organize Lessons with Chapters (Optional)

For long videos (>15 min), add chapter markers:

1. In lesson settings, find **"Marcadores de Capítulo"** (Chapter Markers)
2. Click **"+ Adicionar Marcador"**
3. Set timestamp (e.g., 00:03:45)
4. Add chapter title (e.g., "Passo 2: Instalação")
5. Repeat for each chapter (every 2-3 min recommended)
6. Chapters appear in player seekbar (students can jump to specific sections)
7. Save markers

**Example Chapter Structure for 20-min video:**
- 00:00 - Introdução
- 00:02:30 - Passo 1: Setup Inicial
- 00:06:15 - Passo 2: Configuração Avançada
- 00:12:00 - Passo 3: Teste e Validação
- 00:17:30 - Recap e Próximos Passos

---

#### STEP 9: Test Video Playback

**Critical**: Always test before students see it.

1. Open Hotmart Club in **incognito window** (to simulate student view)
2. Log in with test student account (create one if needed)
3. Navigate to lesson with newly uploaded video
4. Verify:
   - [ ] Video loads within 3-5 seconds
   - [ ] Quality is 1080p/720p (check player settings)
   - [ ] Audio sync is correct (no delay)
   - [ ] Captions display correctly (if uploaded)
   - [ ] Watermark shows student email (if enabled)
   - [ ] Seekbar works (if enabled)
   - [ ] Fullscreen works
   - [ ] Mobile playback (test on phone)
   - [ ] No buffering issues (if yes: reduce bitrate and re-upload)
5. If issues: Re-upload video with corrected settings

---

#### STEP 10: Bulk Upload (For Multiple Videos)

If uploading 10+ videos:

1. Upload all to **Biblioteca de Vídeos** first (parallel uploads possible)
2. Create Excel/Google Sheet with:
   - Column A: Module number
   - Column B: Lesson number
   - Column C: Video title
   - Column D: Video filename
   - Column E: Transcript filename
3. Upload videos in batches of 5 (avoid overwhelming processing queue)
4. While batch 1 processes, prep batch 2
5. Once processed, add to lessons in bulk:
   - Hotmart → Conteúdo → Importar Conteúdo (Import Content)
   - Upload CSV with structure mapping
   - Review and confirm import
6. Verify random sample lessons (10-15%) for quality check

---

### C - Constraints

**Technical Limits:**
- Max file size: 5GB per video (compress if larger)
- Max library size: Unlimited (fair use, ~500-1000 videos typical)
- Processing time: 5-30 min per video (1080p takes longer than 720p)
- Concurrent uploads: 5-10 max (more may cause timeouts)

**Format Requirements:**
- Video codec: H.264 (REQUIRED)
- Audio codec: AAC (REQUIRED)
- Container: MP4 (recommended), MOV (acceptable), AVI (not ideal)
- Resolution: 720p minimum, 1080p recommended, 4K not supported efficiently
- Frame rate: 24fps, 30fps, or 60fps (30fps recommended)
- Aspect ratio: 16:9 (standard widescreen)

**DRM Limitations:**
- DRM only works on Hotmart Player (not external embeds)
- Screen recording can still be done (DRM is not foolproof)
- Watermark deters but doesn't prevent sharing

**Best Practices:**
- ✅ Upload during off-peak hours (faster processing)
- ✅ Use consistent naming: M1A1, M1A2, M2A1 (easy to organize)
- ✅ Test on mobile (40-60% of students watch on phones)
- ✅ Enable adaptive quality (handles slow connections)
- ❌ Don't upload raw footage (compress first with Handbrake)
- ❌ Don't use external embeds for main content (no DRM)
- ❌ Don't skip transcripts (accessibility + SEO)

---

### E - Example

**Scenario**: Uploading 30 videos for "Curso CODEXA - Módulo Anúncios"

**Input:**
- 30 MP4 files (1080p, H.264, 8-12 min each)
- 30 .SRT transcript files
- Module structure: 6 modules, 5 lessons each

**Execution:**

**Day 1 (Setup):**
1. Create module structure in Club (Módulo 1-6)
2. Upload all 30 videos to Biblioteca de Vídeos (2-3 hours with good internet)
3. While processing, review transcripts for accuracy

**Day 2 (Configuration):**
4. Once all videos processed, configure DRM settings:
   - Enable DRM: ✅
   - Watermark: ✅ (email overlay, 60% opacity, bottom right)
   - Block external access: ✅
   - Allow download: ❌
5. Upload transcripts to each video (30 × 2 min = 1 hour)
6. Set custom thumbnails (optional, pre-designed in Canva)

**Day 3 (Lesson Assembly):**
7. Add videos to lessons:
   - Módulo 1: Assign M1A1.mp4, M1A2.mp4... to Aulas 1-5
   - Repeat for Módulos 2-6
8. Attach PDFs/templates to relevant lessons
9. Set lessons 1-2 as mandatory, rest as optional

**Day 4 (Testing & Launch):**
10. Test with fake student account:
   - Random sample: Lessons 1, 5, 10, 15, 20, 25, 30
   - Verify playback, captions, watermark, mobile
11. Fix any issues (re-upload if needed)
12. Configure gotejamento (drip): Week 1 = Modules 1-2, Week 2 = Module 3, etc.
13. Go live

**Output:**
- 30 videos uploaded, protected with DRM, transcripts enabled
- Organized in 6 modules, 5 lessons each
- Tested and ready for students
- Gotejamento configured for weekly release

**Time Investment**: ~8-10 hours (spread over 4 days)

---

## 🎯 SUCCESS CHECKLIST

Before marking upload complete, verify:

- [ ] All videos uploaded to Biblioteca de Vídeos
- [ ] Processing completed (no "Em Processamento" status)
- [ ] DRM enabled on all videos
- [ ] Watermark configured (email overlay)
- [ ] Transcripts uploaded and synced
- [ ] Player settings optimized (seekbar, speed control)
- [ ] Videos assigned to correct lessons
- [ ] Lesson titles and descriptions added
- [ ] Attachments (PDFs) linked to lessons
- [ ] Test student account verified playback
- [ ] Mobile playback tested (iOS and Android if possible)
- [ ] No buffering or loading issues

---

## 🚨 TROUBLESHOOTING

**Problem 1: Video stuck in "Processando" (Processing) for >1 hour**
- **Cause**: File too large, unsupported codec, or server queue backlog
- **Solution**:
  - Check file size (<5GB)
  - Verify codec: H.264 (use MediaInfo tool)
  - Contact Hotmart support: suporte@hotmart.com
  - Re-upload with compressed file (Handbrake: RF 23, H.264, 1080p)

**Problem 2: Video plays but no audio**
- **Cause**: Audio codec not AAC, or audio track missing
- **Solution**:
  - Re-export video with AAC audio (Adobe Premiere, Handbrake)
  - Check audio track exists (use VLC → Tools → Codec Information)

**Problem 3: Captions out of sync**
- **Cause**: .SRT timestamps don't match video edits
- **Solution**:
  - Open .SRT in Subtitle Edit
  - Adjust offset (+/- seconds)
  - Re-upload corrected .SRT

**Problem 4: Watermark not showing**
- **Cause**: DRM disabled or external embed used
- **Solution**:
  - Verify video is from Hotmart library (not YouTube embed)
  - Enable DRM in video settings
  - Re-save player configuration

**Problem 5: Slow playback/buffering**
- **Cause**: Bitrate too high for student's connection
- **Solution**:
  - Enable adaptive quality (auto-adjusts)
  - Re-encode video with lower bitrate (4-6 Mbps for 1080p)
  - Provide 720p version as alternative

---

## 📚 REFERENCES

**Official Hotmart Guides:**
- Upload Videos: https://help.hotmart.com/pt-br/article/360038835051
- Player Configuration: https://help.hotmart.com/pt-br/article/217150538
- Video Library: https://help.hotmart.com/pt-br/article/360038450972
- Embed Videos: https://help.hotmart.com/pt-br/article/208655117

**Tools:**
- **Handbrake**: Free video compression (handbrake.fr)
- **Subtitle Edit**: Free SRT editor (nikse.dk/subtitleedit)
- **MediaInfo**: Check video codec/bitrate (mediaarea.net)
- **Canva**: Create custom thumbnails (canva.com)

**Recommended Video Export Settings (Adobe Premiere/Final Cut):**
- Format: H.264
- Resolution: 1920x1080 (1080p)
- Frame Rate: 30fps
- Bitrate: 6-8 Mbps (CBR or VBR 2-pass)
- Audio: AAC, 192 kbps, Stereo
- Max file size: <5GB (for 30min video)

---

**Version**: 1.0.0
**Created**: 2025-11-20
**TAC-7**: ✅ Compliant
**Integration-Ready**: ✅ Yes
**Tested**: ✅ Production-Ready

**🎬 Upload Complete | 🔒 DRM Protected | 📊 Optimized for Completion**

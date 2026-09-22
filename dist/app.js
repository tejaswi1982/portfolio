// Progressive enhancement: every project and artwork remains available without JS.
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
for (const carousel of document.querySelectorAll('.carousel')) {
  const rail = carousel.querySelector('.slides');
  const slides = [...rail.children];
  const prev = carousel.querySelector('[data-step="-1"]');
  const next = carousel.querySelector('[data-step="1"]');
  const counter = carousel.querySelector('.counter');
  let index = 0;
  const sync = () => {
    index = Math.max(0, Math.min(slides.length - 1, Math.round(rail.scrollLeft / rail.clientWidth)));
    counter.textContent = `${String(index + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
    prev.disabled = index === 0; next.disabled = index === slides.length - 1;
    slides.forEach((slide, i) => { slide.querySelector('button').tabIndex = i === index ? 0 : -1; });
  };
  const move = delta => {
    const target = Math.max(0, Math.min(slides.length - 1, index + delta));
    rail.scrollTo({ left: target * rail.clientWidth, behavior: reduced ? 'instant' : 'smooth' });
  };
  prev.addEventListener('click', () => move(-1)); next.addEventListener('click', () => move(1));
  carousel.addEventListener('keydown', ev => {
    if (ev.key === 'ArrowLeft' || ev.key === 'ArrowRight') { ev.preventDefault(); move(ev.key === 'ArrowLeft' ? -1 : 1); }
    if (ev.key === 'Home' || ev.key === 'End') { ev.preventDefault(); move(ev.key === 'Home' ? -slides.length : slides.length); }
  });
  rail.addEventListener('scroll', sync, { passive: true });
  let width = rail.clientWidth;
  new ResizeObserver(() => { if (rail.clientWidth !== width) { width = rail.clientWidth; rail.scrollTo({left:index*width,behavior:'instant'}); } }).observe(rail);
  sync();
}
const box = document.querySelector('#lightbox');
let opener;
for (const button of document.querySelectorAll('[data-enlarge]')) {
  button.addEventListener('click', () => {
    opener = button;
    box.querySelector('img').src = button.dataset.enlarge;
    box.querySelector('img').alt = button.dataset.caption || '';
    box.querySelector('p').textContent = button.dataset.caption || '';
    box.showModal(); document.body.style.overflow = 'hidden';
  });
}
box?.querySelector('.close-lightbox').addEventListener('click', () => box.close());
box?.addEventListener('click', ev => { if (ev.target === box) { const r=box.getBoundingClientRect(); if(ev.clientX<r.left||ev.clientX>r.right||ev.clientY<r.top||ev.clientY>r.bottom)box.close(); } });
box?.addEventListener('close', () => { document.body.style.overflow = ''; opener?.focus({preventScroll:true}); });
for (const filters of document.querySelectorAll('.filters')) {
  const rows = [...filters.nextElementSibling.querySelectorAll('.work-row')];
  const status = filters.parentElement.querySelector('.filter-result');
  for (const button of filters.querySelectorAll('button')) button.addEventListener('click', () => {
    const category = button.dataset.filter;
    filters.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b===button)));
    let count = 0;
    rows.forEach(row => { row.hidden = category !== 'all' && !row.dataset.category.split(' ').includes(category); if (!row.hidden) count++; });
    if (status) status.textContent = `${count} ${count===1?'project':'projects'}`;
  });
}
// Avoid overlapping soundtracks; playback always starts with a user action.
for (const video of document.querySelectorAll('video')) {
  video.addEventListener('play', () => document.querySelectorAll('video').forEach(other => { if (other !== video) other.pause(); }));
  video.addEventListener('error', () => {
    if(video.nextElementSibling?.classList.contains('video-error'))return;
    const message=document.createElement('p');message.className='video-error';message.textContent='This film could not load. ';
    const link=document.createElement('a');link.href=video.querySelector('source').src;link.textContent='Open the film directly ↗';message.append(link);video.after(message);
  });
}

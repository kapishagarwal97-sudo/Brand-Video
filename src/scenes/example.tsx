import {
  makeScene2D,
  Rect,
  Circle,
  Img,
  Txt,
  Layout,
  Gradient,
  blur,
  brightness,
} from '@motion-canvas/2d';
import {
  all,
  chain,
  loop,
  waitFor,
  easeInOutCubic,
  easeInOutSine,
  easeOutCubic,
  easeInCubic,
  easeOutBack,
} from '@motion-canvas/core';

/*
 * TRYB — Modern SaaS Brand Launch Film
 * =========================================================================
 * Format : 9:16 vertical, 1080 x 1920 (set this in Video Settings).
 * Vibe   : deep dark-mode space, ambient indigo glow, layered "floating
 *          card" compositions, a continuous cinematic camera push, spring
 *          entrances and kinetic staggered typography.
 * Layout : full-bleed blurred backdrop → layered UI cards up top →
 *          kinetic headline block anchored to the lower third.
 * =========================================================================
 */

// Scene 1 — Hook
import s1_scrolling from './assets/tryb/s1_scrolling.png';
import s1_notifications from './assets/tryb/s1_notifications.png';
import s1_deadchats from './assets/tryb/s1_deadchats.png';
import s1_calendar from './assets/tryb/s1_calendar.png';
import s1_cafe from './assets/tryb/s1_cafe.png';
// Scene 2 — Problem
import s2_cancelling from './assets/tryb/s2_cancelling.png';
import s2_dating from './assets/tryb/s2_dating.png';
import s2_instagram from './assets/tryb/s2_instagram.png';
import s2_couple from './assets/tryb/s2_couple.png';
import s2_weekend from './assets/tryb/s2_weekend.png';
// Scene 3 — Idea
import s3_logo from './assets/tryb/s3_logo.png';
import s3_questions from './assets/tryb/s3_questions.png';
import s3_invite from './assets/tryb/s3_invite.png';
import s3_coffee from './assets/tryb/s3_coffee.png';
import s3_hiking from './assets/tryb/s3_hiking.png';
import s3_dinner from './assets/tryb/s3_dinner.png';
import s3_pottery from './assets/tryb/s3_pottery.png';
import s3_boardgames from './assets/tryb/s3_boardgames.png';
// Scene 4 — How It Works
import s4_answers from './assets/tryb/s4_answers.png';
import s4_matches from './assets/tryb/s4_matches.png';
import s4_invite from './assets/tryb/s4_invite.png';
import s4_gathering from './assets/tryb/s4_gathering.png';
// Scene 5 — Emotion
import s5_laughter from './assets/tryb/s5_laughter.png';
import s5_sunset from './assets/tryb/s5_sunset.png';
import s5_coffeechat from './assets/tryb/s5_coffeechat.png';
import s5_walking from './assets/tryb/s5_walking.png';
// Scene 6 — Ending
import s6_logo from './assets/tryb/s6_logo.png';
import s6_website from './assets/tryb/s6_website.png';

// ---------------------------------------------------------------------------
// Design tokens
// ---------------------------------------------------------------------------
const BG = '#0B0B0F';
const INDIGO = '#4F46E5';
const INK = '#F6F6F9';
const MUTED = '#9A98B0';
const CREAM = '#F2E6CF';
const FONT = 'Inter, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif';

export default makeScene2D(function* (view) {
  const W = 1080;
  const H = 1920;

  // =========================================================================
  // Ambient stage: background, pulsing glow, world container, scrim, vignette
  // =========================================================================
  view.add(<Rect width={W} height={H} fill={BG} zIndex={-20} />);

  const glow = (
    <Circle
      width={1600}
      height={1600}
      y={-140}
      zIndex={-18}
      opacity={0.15}
      fill={
        new Gradient({
          type: 'radial',
          from: [0, 0],
          to: [0, 0],
          fromRadius: 0,
          toRadius: 800,
          stops: [
            {offset: 0, color: INDIGO},
            {offset: 0.55, color: '#4F46E5cc'},
            {offset: 1, color: '#4F46E500'},
          ],
        })
      }
    />
  ) as Circle;
  view.add(glow);

  // A soft second glow, lower and warmer, for depth
  view.add(
    <Circle
      width={1100}
      height={1100}
      x={-260}
      y={620}
      zIndex={-19}
      opacity={0.1}
      fill={
        new Gradient({
          type: 'radial',
          from: [0, 0],
          to: [0, 0],
          fromRadius: 0,
          toRadius: 550,
          stops: [
            {offset: 0, color: '#7C5CFF'},
            {offset: 1, color: '#7C5CFF00'},
          ],
        })
      }
    />,
  );

  const world = (<Layout />) as Layout;
  view.add(world);

  // Persistent film vignette
  view.add(
    <Rect
      width={W}
      height={H}
      zIndex={40}
      opacity={0.55}
      fill={
        new Gradient({
          type: 'radial',
          from: [0, 0],
          to: [0, 0],
          fromRadius: 380,
          toRadius: 1200,
          stops: [
            {offset: 0, color: '#00000000'},
            {offset: 1, color: '#000000dd'},
          ],
        })
      }
    />,
  );

  // Gentle, endless breathing pulse on the ambient glow
  yield loop(function* () {
    yield* all(glow.scale(1.18, 3.6, easeInOutSine), glow.opacity(0.22, 3.6, easeInOutSine));
    yield* all(glow.scale(1.0, 3.6, easeInOutSine), glow.opacity(0.13, 3.6, easeInOutSine));
  });

  // =========================================================================
  // Helpers
  // =========================================================================

  // A styled, glassy "floating card" image with soft drop-shadow + hairline.
  function card(
    parent: Layout,
    src: string,
    opts: {
      w: number;
      x?: number;
      y?: number;
      rot?: number;
      z?: number;
      radius?: number;
      filters?: any[];
      opacity?: number;
    },
  ): Img {
    const n = (
      <Img
        src={src}
        width={opts.w}
        x={opts.x ?? 0}
        y={opts.y ?? 0}
        rotation={opts.rot ?? 0}
        zIndex={opts.z ?? 1}
        radius={opts.radius ?? 30}
        opacity={opts.opacity ?? 1}
        filters={opts.filters ?? []}
        stroke={'rgba(255,255,255,0.14)'}
        lineWidth={1.5}
        shadowColor={'rgba(0,0,0,0.75)'}
        shadowBlur={90}
        shadowOffset={[0, 40]}
      />
    ) as Img;
    parent.add(n);
    return n;
  }

  // Full-bleed, heavily blurred + dimmed backdrop for depth.
  function backdrop(parent: Layout, src: string): Img {
    const n = (
      <Img
        src={src}
        height={H + 240}
        zIndex={-2}
        opacity={0}
        filters={[blur(60), brightness(0.4)]}
      />
    ) as Img;
    parent.add(n);
    return n;
  }

  // Bottom scrim so the headline stays crisp over any imagery.
  function scrim(parent: Layout) {
    parent.add(
      <Rect
        width={W}
        height={1000}
        y={H / 2 - 500}
        zIndex={8}
        fill={
          new Gradient({
            type: 'linear',
            from: [0, -500],
            to: [0, 500],
            stops: [
              {offset: 0, color: '#0B0B0F00'},
              {offset: 0.62, color: '#0B0B0Fcc'},
              {offset: 1, color: '#0B0B0Fff'},
            ],
          })
        }
      />,
    );
  }

  // Spring-ish entrance: slide up + fade (+ optional scale pop).
  function* enter(
    node: Layout | Img | Txt,
    opts: {dy?: number; dur?: number; delay?: number; scaleFrom?: number} = {},
  ) {
    const dy = opts.dy ?? 90;
    const dur = opts.dur ?? 0.7;
    const ty = node.y();
    const to = node.opacity();
    node.y(ty + dy);
    node.opacity(0);
    const anims: any[] = [
      node.y(ty, dur, easeOutCubic),
      node.opacity(to, dur, easeOutCubic),
    ];
    if (opts.scaleFrom != null) {
      node.scale(opts.scaleFrom);
      anims.push(node.scale(1, dur, easeOutBack));
    }
    yield* chain(waitFor(opts.delay ?? 0), all(...anims));
  }

  // Stagger a set of nodes in with a shared cadence.
  function* enterStagger(
    nodes: (Layout | Img | Txt)[],
    opts: {dy?: number; dur?: number; stagger?: number; scaleFrom?: number} = {},
  ) {
    const stagger = opts.stagger ?? 0.15;
    yield* all(
      ...nodes.map((n, i) => enter(n, {...opts, delay: i * stagger})),
    );
  }

  // Continuous, endless soft bob for "alive" floating cards.
  function bob(node: Img, amp = 14, period = 3) {
    const baseY = node.y();
    return loop(function* () {
      yield* node.y(baseY + amp, period, easeInOutSine);
      yield* node.y(baseY - amp, period, easeInOutSine);
    });
  }

  // Build a kinetic, staggered headline block anchored to the lower third.
  function headline(
    parent: Layout,
    lines: {t: string; size?: number; weight?: number; fill?: string}[],
    opts: {y?: number; align?: 'center' | 'left'} = {},
  ): Txt[] {
    const baseY = opts.y ?? 660;
    const align = opts.align ?? 'center';
    // measure total block height first
    const heights = lines.map((l) => (l.size ?? 62) * 1.14);
    const gap = 6;
    const total = heights.reduce((a, b) => a + b, 0) + gap * (lines.length - 1);
    let cursor = baseY - total / 2;
    const txts: Txt[] = [];
    for (let i = 0; i < lines.length; i++) {
      const l = lines[i];
      const h = heights[i];
      const t = (
        <Txt
          text={l.t}
          x={align === 'left' ? -470 : 0}
          y={cursor + h / 2}
          width={960}
          textAlign={align}
          textWrap
          zIndex={10}
          opacity={0}
          fontFamily={FONT}
          fontWeight={l.weight ?? 800}
          fontSize={l.size ?? 62}
          lineHeight={h}
          letterSpacing={-0.5}
          fill={l.fill ?? INK}
          shadowColor={'#000000'}
          shadowBlur={24}
        />
      ) as Txt;
      parent.add(t);
      txts.push(t);
      cursor += h + gap;
    }
    return txts;
  }

  function* revealHeadline(txts: Txt[], stagger = 0.15) {
    yield* all(
      ...txts.map((t, i) =>
        chain(
          waitFor(i * stagger),
          all(t.opacity(1, 0.6, easeOutCubic), t.y(t.y() - 34, 0.6, easeOutCubic)),
        ),
      ),
    );
  }

  // Exit a whole scene with a subtle "push through the lens".
  function* outScene(root: Layout, dur = 0.6) {
    yield* all(
      root.opacity(0, dur, easeInOutCubic),
      root.scale(root.scale().x * 1.08, dur, easeInCubic),
    );
    root.remove();
  }

  // Create a scene container + start its slow camera push. Returns the node.
  function newScene(): Layout {
    const root = (<Layout />) as Layout;
    world.add(root);
    root.scale(1.0);
    return root;
  }

  // =========================================================================
  // SCENE 1 — HOOK  (layered phone UI + floating notifications)
  // =========================================================================
  yield* (function* () {
    const dur = 13;
    const s = newScene();
    yield s.scale(1.05, dur, easeInOutSine); // continuous cinematic camera push
    const bd = backdrop(s, s1_cafe);

    // Hero device, skewed slightly, dead center-top
    const hero = card(s, s1_scrolling, {w: 500, x: -20, y: -360, rot: -5, z: 5});
    // Floating UI cards that pop on top
    const notif = card(s, s1_notifications, {w: 360, x: 240, y: -560, rot: 6, z: 7});
    const dead = card(s, s1_deadchats, {w: 330, x: -250, y: -170, rot: -8, z: 6});
    const cal = card(s, s1_calendar, {w: 300, x: 250, y: -110, rot: 9, z: 4, opacity: 0.96});
    scrim(s);

    const head = headline(s, [
      {t: 'We’ve never been', size: 64, fill: MUTED, weight: 600},
      {t: 'more connected.', size: 78, fill: INK},
      {t: 'Yet never more alone.', size: 52, fill: MUTED, weight: 500},
    ]);

    // Choreography
    yield* all(bd.opacity(0.55, 1.0), enter(hero, {dy: 70, scaleFrom: 0.9, dur: 0.9}));
    yield* enterStagger([notif, dead, cal], {dy: 110, stagger: 0.18, scaleFrom: 0.86});
    yield loop(function* () { yield* bob(notif, 16, 3.2); });
    yield loop(function* () { yield* bob(dead, 12, 3.6); });
    yield* revealHeadline(head);
    yield* waitFor(dur - 6.0);
    yield* outScene(s);
  })();

  // =========================================================================
  // SCENE 2 — THE PROBLEM  (couple on phones, dating + social floaters)
  // =========================================================================
  yield* (function* () {
    const dur = 14;
    const s = newScene();
    yield s.scale(1.05, dur, easeInOutSine); // continuous cinematic camera push
    const bd = backdrop(s, s2_weekend);

    const hero = card(s, s2_couple, {w: 560, x: 0, y: -330, rot: 3, z: 5});
    const dating = card(s, s2_dating, {w: 300, x: -260, y: -520, rot: -9, z: 7});
    const insta = card(s, s2_instagram, {w: 250, x: 270, y: -150, rot: 8, z: 6});
    const cancel = card(s, s2_cancelling, {w: 300, x: -250, y: -110, rot: -6, z: 4, opacity: 0.96});
    scrim(s);

    const head = headline(s, [
      {t: 'Making plans', size: 72, fill: INK},
      {t: 'shouldn’t feel like work.', size: 54, fill: MUTED, weight: 600},
      {t: 'The right people shouldn’t', size: 44, fill: MUTED, weight: 500},
      {t: 'be left to chance.', size: 44, fill: MUTED, weight: 500},
    ]);

    yield* all(bd.opacity(0.5, 1.0), enter(hero, {dy: 80, scaleFrom: 0.9, dur: 0.9}));
    yield* enterStagger([dating, insta, cancel], {dy: 120, stagger: 0.16, scaleFrom: 0.85});
    yield loop(function* () { yield* bob(dating, 15, 3.1); });
    yield loop(function* () { yield* bob(insta, 12, 3.5); });
    yield* revealHeadline(head);
    yield* waitFor(dur - 6.4);
    yield* outScene(s);
  })();

  // =========================================================================
  // SCENE 3 — THE IDEA  (brand reveal + fanned experience gallery)
  // =========================================================================
  yield* (function* () {
    const dur = 16;
    const s = newScene();
    yield s.scale(1.05, dur, easeInOutSine); // continuous cinematic camera push
    const bd = backdrop(s, s3_invite);

    // Brand wordmark, front and center
    const logo = (
      <Txt
        text={'TRYB'}
        y={-620}
        zIndex={9}
        opacity={0}
        fontFamily={FONT}
        fontWeight={900}
        fontSize={150}
        letterSpacing={12}
        fill={INK}
        shadowColor={INDIGO}
        shadowBlur={60}
      />
    ) as Txt;
    s.add(logo);

    // Fanned gallery of the five real experiences
    const exp = [
      card(s, s3_coffee, {w: 260, x: -360, y: -300, rot: -12, z: 4}),
      card(s, s3_hiking, {w: 270, x: -180, y: -360, rot: -6, z: 5}),
      card(s, s3_dinner, {w: 290, x: 0, y: -390, rot: 0, z: 7}),
      card(s, s3_pottery, {w: 270, x: 185, y: -360, rot: 6, z: 5}),
      card(s, s3_boardgames, {w: 260, x: 360, y: -300, rot: 12, z: 4}),
    ];
    // Supporting product floaters
    const q = card(s, s3_questions, {w: 240, x: -280, y: -70, rot: -7, z: 6});
    const inv = card(s, s3_invite, {w: 250, x: 280, y: -60, rot: 8, z: 6});
    scrim(s);

    const head = headline(s, [
      {t: 'Not another social app.', size: 46, fill: MUTED, weight: 600},
      {t: 'A better way to', size: 70, fill: INK},
      {t: 'experience real life.', size: 70, fill: CREAM},
    ]);

    yield* all(
      bd.opacity(0.5, 1.0),
      enter(logo, {dy: 50, scaleFrom: 0.7, dur: 1.0}),
    );
    yield* enterStagger(exp, {dy: 130, stagger: 0.12, scaleFrom: 0.8, dur: 0.7});
    yield* enterStagger([q, inv], {dy: 90, stagger: 0.15, scaleFrom: 0.85});
    yield loop(function* () { yield* bob(exp[2], 14, 3.4); });
    yield* revealHeadline(head);
    yield* waitFor(dur - 8.0);
    yield* outScene(s);
  })();

  // =========================================================================
  // SCENE 4 — HOW IT WORKS  (AI curation graph as hero, product floaters)
  // =========================================================================
  yield* (function* () {
    const dur = 15;
    const s = newScene();
    yield s.scale(1.05, dur, easeInOutSine); // continuous cinematic camera push
    const bd = backdrop(s, s4_gathering);

    const graph = card(s, s4_matches, {w: 560, x: 0, y: -360, rot: 0, z: 5});
    const answers = card(s, s4_answers, {w: 300, x: -260, y: -560, rot: -8, z: 6});
    const invite = card(s, s4_invite, {w: 320, x: 250, y: -150, rot: 7, z: 7});
    const group = card(s, s4_gathering, {w: 340, x: -240, y: -100, rot: -5, z: 4, opacity: 0.97});
    scrim(s);

    const head = headline(s, [
      {t: 'Tell us who you are.', size: 58, fill: INK},
      {t: 'We curate the people.', size: 58, fill: INK},
      {t: 'You simply show up.', size: 58, fill: CREAM},
    ]);

    yield* all(bd.opacity(0.5, 1.0), enter(graph, {dy: 80, scaleFrom: 0.9, dur: 0.9}));
    yield* enterStagger([answers, invite, group], {dy: 120, stagger: 0.16, scaleFrom: 0.85});
    yield loop(function* () { yield* bob(invite, 16, 3.0); });
    yield loop(function* () { yield* bob(answers, 12, 3.6); });
    // Steps reveal one-by-one, a touch slower for rhythm
    yield* revealHeadline(head, 0.9);
    yield* waitFor(dur - 8.0);
    yield* outScene(s);
  })();

  // =========================================================================
  // SCENE 5 — THE EMOTION  (warm human gallery)
  // =========================================================================
  yield* (function* () {
    const dur = 14;
    const s = newScene();
    yield s.scale(1.05, dur, easeInOutSine); // continuous cinematic camera push
    const bd = backdrop(s, s5_sunset);

    const hero = card(s, s5_laughter, {w: 560, x: 0, y: -340, rot: -3, z: 5});
    const chat = card(s, s5_coffeechat, {w: 300, x: 260, y: -540, rot: 8, z: 7});
    const walk = card(s, s5_walking, {w: 300, x: -260, y: -150, rot: -7, z: 6});
    const sun = card(s, s5_sunset, {w: 300, x: 250, y: -110, rot: 6, z: 4, opacity: 0.97});
    scrim(s);

    const head = headline(s, [
      {t: 'The best memories', size: 60, fill: MUTED, weight: 600},
      {t: 'aren’t made online —', size: 60, fill: INK},
      {t: 'they’re made in real life.', size: 60, fill: CREAM},
    ]);

    yield* all(bd.opacity(0.55, 1.0), enter(hero, {dy: 80, scaleFrom: 0.9, dur: 0.9}));
    yield* enterStagger([chat, walk, sun], {dy: 120, stagger: 0.16, scaleFrom: 0.85});
    yield loop(function* () { yield* bob(chat, 15, 3.2); });
    yield loop(function* () { yield* bob(walk, 12, 3.6); });
    yield* revealHeadline(head);
    yield* waitFor(dur - 6.4);
    yield* outScene(s);
  })();

  // =========================================================================
  // SCENE 6 — ENDING  (logo lockup, tagline, product, CTA)
  // =========================================================================
  yield* (function* () {
    const dur = 11;
    const s = newScene();
    yield s.scale(1.05, dur, easeInOutSine); // continuous cinematic camera push
    const bd = backdrop(s, s6_website);

    const logo = card(s, s6_logo, {w: 560, x: 0, y: -520, rot: 0, z: 6, radius: 34});
    const device = card(s, s6_website, {w: 620, x: 0, y: -60, rot: 0, z: 5});
    scrim(s);

    const head = headline(
      s,
      [
        {t: 'Welcome to TRYB.', size: 82, fill: INK},
        {t: 'Your people are out there.', size: 46, fill: MUTED, weight: 500},
      ],
      {y: 560},
    );

    // Call-to-action pill
    const pill = (
      <Rect
        y={780}
        width={380}
        height={112}
        radius={56}
        zIndex={11}
        fill={CREAM}
        opacity={0}
        scale={0}
        shadowColor={'rgba(79,70,229,0.5)'}
        shadowBlur={60}
        shadowOffset={[0, 18]}
      >
        <Txt text={'Join TRYB'} fontFamily={FONT} fontWeight={700} fontSize={46} fill={'#141018'} />
      </Rect>
    ) as Rect;
    s.add(pill);

    yield* all(bd.opacity(0.5, 1.0), enter(logo, {dy: 60, scaleFrom: 0.8, dur: 1.0}));
    yield* enter(device, {dy: 120, scaleFrom: 0.88, dur: 0.8});
    yield* revealHeadline(head, 0.18);
    yield* all(pill.scale(1, 0.6, easeOutBack), pill.opacity(1, 0.4));
    // Subtle idle life on the CTA
    yield loop(function* () {
      yield* pill.scale(1.04, 1.1, easeInOutSine);
      yield* pill.scale(1.0, 1.1, easeInOutSine);
    });
    yield* waitFor(dur - 6.0);

    // Final slow fade to black
    yield* all(s.opacity(0, 1.3, easeInOutCubic), s.scale(1.12, 1.3, easeInCubic));
    s.remove();
  })();
});

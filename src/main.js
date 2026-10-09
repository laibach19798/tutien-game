(async function(){
  const T=Tutien,cv=document.getElementById('game'),ctx=cv.getContext('2d'),hud=document.getElementById('hud');
  const assets=new T.AssetManager();
  try{await assets.load(T.ASSET_MANIFEST);}catch(e){hud.textContent=e.message;return;}
  const sz=document.getElementById('stick'),stick=sz?new T.TouchStick(sz,document.getElementById('knob')):null;
  const input=new T.Input(stick),world=new T.World(assets),camera=new T.Camera();
  const player=new T.Player(assets,world.spawn.x,world.spawn.y);
  const keyMap={};addEventListener('keydown',e=>{if(keyMap[e.code]&&!e.repeat)keyMap[e.code]();});
  const stage=cv.parentElement;
  const resize=()=>{cv.width=stage.clientWidth;cv.height=stage.clientHeight;camera.resize(cv.width,cv.height);};
  addEventListener('resize',resize);resize();
  const slots={hair:'Tóc',clothes:'Áo',shoes:'Giày',weapon:'Kiếm'},wd=document.getElementById('wardrobe');
  if(wd)T.EQUIP_SLOTS.slice().reverse().forEach((slot,i)=>{
    const b=document.createElement('button');b.type='button';b.id='eq-'+slot;
    const multi=Object.values(T.ITEMS).filter(it=>it.slot===slot).length>1; // slot có nhiều món -> bấm để đổi món
    const sync=()=>{const id=player.equipped[slot];b.className=id?'on':'';b.textContent=multi&&id?T.ITEMS[id].name:slots[slot];};
    const act=()=>{multi?player.cycle(slot):player.toggle(slot);sync();};
    b.addEventListener('click',act);sync();wd.appendChild(b);
    keyMap['Digit'+(i+1)]=act;
  });
  const ab=document.getElementById('btn-attack');
  if(ab){ab.addEventListener('pointerdown',e=>{input.pressAttack();e.preventDefault();});}
  const jb=document.getElementById('btn-jump');
  if(jb){jb.addEventListener('pointerdown',e=>{input.pressJump();e.preventDefault();});}
  camera.follow(player,{w:world.w,h:world.h});
  const touch=matchMedia('(pointer:coarse)').matches;
  let last=performance.now(),fps=60;
  function frame(now){
    const dt=Math.min((now-last)/1000,0.05);last=now;fps+=(1/Math.max(dt,1e-4)-fps)*0.05;
    player.update(dt,input,world);camera.update(dt);
    ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#223';ctx.fillRect(0,0,cv.width,cv.height);
    camera.begin(ctx);const r=camera.rect();world.drawGround(ctx,r);
    const items=world.visibleProps(r);items.push(player);items.sort((a,b)=>a.y-b.y);items.forEach(i=>i.draw(ctx));
    camera.end(ctx);
    hud.textContent=`${touch?'Joystick (đẩy hết cỡ = chạy)':'WASD · Shift chạy · Space nhảy · J chém'} | hướng: ${player.facing} | ${player.anim.name} f${player.anim.frame} | ${fps.toFixed(0)} FPS`;
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();

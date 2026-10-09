(function(T){
T.AssetManager=class{
  constructor(){this.imgs={};}
  load(manifest){
    return Promise.all(Object.entries(manifest).map(([k,p])=>new Promise((res,rej)=>{
      const i=new Image(); i.onload=()=>{this.imgs[k]=i;res();}; i.onerror=()=>rej(new Error('Không tải được '+p)); i.src=p;
    })));
  }
  get(k){return this.imgs[k];}
};
})(window.Tutien=window.Tutien||{});

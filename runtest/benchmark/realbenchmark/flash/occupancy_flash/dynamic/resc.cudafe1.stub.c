#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-function"
#pragma GCC diagnostic ignored "-Wcast-qual"
#define __NV_CUBIN_HANDLE_STORAGE__ static
#if !defined(__CUDA_INCLUDE_COMPILER_INTERNAL_HEADERS__)
#define __CUDA_INCLUDE_COMPILER_INTERNAL_HEADERS__
#endif
#include "crt/host_runtime.h"
#include "resc.fatbin.c"
static void __device_stub__Z29dynamic_mailbox_many_clustersILi2EEvPfP11ClusterMetaS0_iiii(float *__restrict__, struct ClusterMeta *__restrict__, float *__restrict__, int, int, int, int);
static void __device_stub__Z29dynamic_mailbox_many_clustersILi4EEvPfP11ClusterMetaS0_iiii(float *__restrict__, struct ClusterMeta *__restrict__, float *__restrict__, int, int, int, int);
static void __device_stub__Z29dynamic_mailbox_many_clustersILi8EEvPfP11ClusterMetaS0_iiii(float *__restrict__, struct ClusterMeta *__restrict__, float *__restrict__, int, int, int, int);
static void __nv_cudaEntityRegisterCallback(void **);
static void __sti____cudaRegisterAll(void) __attribute__((__constructor__));
static void __device_stub__Z29dynamic_mailbox_many_clustersILi2EEvPfP11ClusterMetaS0_iiii(float *__restrict__ __par0, struct ClusterMeta *__restrict__ __par1, float *__restrict__ __par2, int __par3, int __par4, int __par5, int __par6){ float *__T21;
 struct ClusterMeta *__T22;
 float *__T23;
__cudaLaunchPrologue(7);__T21 = __par0;__cudaSetupArgSimple(__T21, 0UL);__T22 = __par1;__cudaSetupArgSimple(__T22, 8UL);__T23 = __par2;__cudaSetupArgSimple(__T23, 16UL);__cudaSetupArgSimple(__par3, 24UL);__cudaSetupArgSimple(__par4, 28UL);__cudaSetupArgSimple(__par5, 32UL);__cudaSetupArgSimple(__par6, 36UL);__cudaLaunch(((char *)((void ( *)(float *__restrict__, struct ClusterMeta *__restrict__, float *__restrict__, int, int, int, int))dynamic_mailbox_many_clusters<(int)2> )));}
template<> __specialization_static void __wrapper__device_stub_dynamic_mailbox_many_clusters<2>( float *__restrict__ &__cuda_0,struct ::ClusterMeta *__restrict__ &__cuda_1,float *__restrict__ &__cuda_2,int &__cuda_3,int &__cuda_4,int &__cuda_5,int &__cuda_6){__device_stub__Z29dynamic_mailbox_many_clustersILi2EEvPfP11ClusterMetaS0_iiii( (float *&)__cuda_0,(struct ::ClusterMeta *&)__cuda_1,(float *&)__cuda_2,(int &)__cuda_3,(int &)__cuda_4,(int &)__cuda_5,(int &)__cuda_6);}
static void __device_stub__Z29dynamic_mailbox_many_clustersILi4EEvPfP11ClusterMetaS0_iiii(float *__restrict__ __par0, struct ClusterMeta *__restrict__ __par1, float *__restrict__ __par2, int __par3, int __par4, int __par5, int __par6){ float *__T24;
 struct ClusterMeta *__T25;
 float *__T26;
__cudaLaunchPrologue(7);__T24 = __par0;__cudaSetupArgSimple(__T24, 0UL);__T25 = __par1;__cudaSetupArgSimple(__T25, 8UL);__T26 = __par2;__cudaSetupArgSimple(__T26, 16UL);__cudaSetupArgSimple(__par3, 24UL);__cudaSetupArgSimple(__par4, 28UL);__cudaSetupArgSimple(__par5, 32UL);__cudaSetupArgSimple(__par6, 36UL);__cudaLaunch(((char *)((void ( *)(float *__restrict__, struct ClusterMeta *__restrict__, float *__restrict__, int, int, int, int))dynamic_mailbox_many_clusters<(int)4> )));}
template<> __specialization_static void __wrapper__device_stub_dynamic_mailbox_many_clusters<4>( float *__restrict__ &__cuda_0,struct ::ClusterMeta *__restrict__ &__cuda_1,float *__restrict__ &__cuda_2,int &__cuda_3,int &__cuda_4,int &__cuda_5,int &__cuda_6){__device_stub__Z29dynamic_mailbox_many_clustersILi4EEvPfP11ClusterMetaS0_iiii( (float *&)__cuda_0,(struct ::ClusterMeta *&)__cuda_1,(float *&)__cuda_2,(int &)__cuda_3,(int &)__cuda_4,(int &)__cuda_5,(int &)__cuda_6);}
static void __device_stub__Z29dynamic_mailbox_many_clustersILi8EEvPfP11ClusterMetaS0_iiii(float *__restrict__ __par0, struct ClusterMeta *__restrict__ __par1, float *__restrict__ __par2, int __par3, int __par4, int __par5, int __par6){ float *__T27;
 struct ClusterMeta *__T28;
 float *__T29;
__cudaLaunchPrologue(7);__T27 = __par0;__cudaSetupArgSimple(__T27, 0UL);__T28 = __par1;__cudaSetupArgSimple(__T28, 8UL);__T29 = __par2;__cudaSetupArgSimple(__T29, 16UL);__cudaSetupArgSimple(__par3, 24UL);__cudaSetupArgSimple(__par4, 28UL);__cudaSetupArgSimple(__par5, 32UL);__cudaSetupArgSimple(__par6, 36UL);__cudaLaunch(((char *)((void ( *)(float *__restrict__, struct ClusterMeta *__restrict__, float *__restrict__, int, int, int, int))dynamic_mailbox_many_clusters<(int)8> )));}
template<> __specialization_static void __wrapper__device_stub_dynamic_mailbox_many_clusters<8>( float *__restrict__ &__cuda_0,struct ::ClusterMeta *__restrict__ &__cuda_1,float *__restrict__ &__cuda_2,int &__cuda_3,int &__cuda_4,int &__cuda_5,int &__cuda_6){__device_stub__Z29dynamic_mailbox_many_clustersILi8EEvPfP11ClusterMetaS0_iiii( (float *&)__cuda_0,(struct ::ClusterMeta *&)__cuda_1,(float *&)__cuda_2,(int &)__cuda_3,(int &)__cuda_4,(int &)__cuda_5,(int &)__cuda_6);}
static void __nv_cudaEntityRegisterCallback(void **__T73){__nv_dummy_param_ref(__T73);__nv_save_fatbinhandle_for_managed_rt(__T73);__cudaRegisterEntry(__T73, ((void ( *)(float *__restrict__, struct ClusterMeta *__restrict__, float *__restrict__, int, int, int, int))dynamic_mailbox_many_clusters<(int)8> ), _Z29dynamic_mailbox_many_clustersILi8EEvPfP11ClusterMetaS0_iiii, (-1));__cudaRegisterEntry(__T73, ((void ( *)(float *__restrict__, struct ClusterMeta *__restrict__, float *__restrict__, int, int, int, int))dynamic_mailbox_many_clusters<(int)4> ), _Z29dynamic_mailbox_many_clustersILi4EEvPfP11ClusterMetaS0_iiii, (-1));__cudaRegisterEntry(__T73, ((void ( *)(float *__restrict__, struct ClusterMeta *__restrict__, float *__restrict__, int, int, int, int))dynamic_mailbox_many_clusters<(int)2> ), _Z29dynamic_mailbox_many_clustersILi2EEvPfP11ClusterMetaS0_iiii, (-1));__cudaRegisterVariable(__T73, __shadow_var(g_dummy_registration_flag,::g_dummy_registration_flag), 0, 4UL, 0, 0);}
static void __sti____cudaRegisterAll(void){__cudaRegisterBinary(__nv_cudaEntityRegisterCallback);}

#pragma GCC diagnostic pop

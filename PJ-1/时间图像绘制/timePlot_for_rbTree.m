%% initial
init = [0.00200057	0.004001379	0.004000664	0.005000591	0.004000664	0.004001141	0.006001711	0.006000996	0.004001141	0.006001711	0.00500083	0.005001068	0.006000519	0.005002499	0.005004168	0.005001545	0.005002022	0.00500083	0.006000996	0.005001783	0.005001307	0.006000519	0.00500083	0.005001783	0.006000757	0.005001307	0.006001234	0.006001711	0.006000757	0.005001545	0.0070014	0.006002188	0.006000042];

tt = 1:length(init);
tt = 100*tt;

figure()
plot(tt,init,LineWidth=1.5)
title('红黑树每初始化100个单词所用时间')
xlabel('红黑树中的单词数量')
ylabel('每初始化100个单词所用时间') 
saveas(gcf,'rbTree_init.png')
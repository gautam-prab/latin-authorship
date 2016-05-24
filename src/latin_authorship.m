# uses LIBSVM to use machine learning to classify authorship of Latin works
function [retval] = latin_authorship (training_scaled, cross_validation_scaled, test_scaled)
	printf("creating datasets\n")
	[train_lab, train_inst] = libsvmread(training_scaled);
	[cross_lab, cross_inst] = libsvmread(cross_validation_scaled);
	[test_lab, test_inst] = libsvmread(test_scaled);

	# here we create 8 different label sets for each author
	# that way we have 8 different binary classifiers for each author
	# this allows us to find which author wrote a text or if it is none of the above
	# with a multiclass SVM classifier, we can't have a none of the above option
	train_lab_mat = [cast(train_lab == 1, "double"), cast(train_lab == 2, "double"), cast(train_lab == 3, "double"), cast(train_lab == 4, "double"), cast(train_lab == 5, "double"), cast(train_lab == 6, "double"), cast(train_lab == 7, "double"), cast(train_lab == 8, "double")];
	cross_lab_mat = [cast(cross_lab == 1, "double"), cast(cross_lab == 2, "double"), cast(cross_lab == 3, "double"), cast(cross_lab == 4, "double"), cast(cross_lab == 5, "double"), cast(cross_lab == 6, "double"), cast(cross_lab == 7, "double"), cast(cross_lab == 8, "double")];
	test_lab_mat = [cast(test_lab == 1, "double"), cast(test_lab == 2, "double"), cast(test_lab == 3, "double"), cast(test_lab == 4, "double"), cast(test_lab == 5, "double"), cast(test_lab == 6, "double"), cast(test_lab == 7, "double"), cast(test_lab == 8, "double")];

	# create 8 different models for each author
	printf("creating models\n")
	model_mat = [svmtrain(train_lab_mat(:,1), train_inst, '-c 2 -g .0078125 -b 1'); svmtrain(train_lab_mat(:,2), train_inst, '-c 2 -g .0078125 -b 1'); svmtrain(train_lab_mat(:,3), train_inst, '-c 2 -g .0078125 -b 1'); svmtrain(train_lab_mat(:,4), train_inst, '-c 2 -g .0078125 -b 1'); svmtrain(train_lab_mat(:,5), train_inst, '-c 2 -g .0078125 -b 1'); svmtrain(train_lab_mat(:,6), train_inst, '-c 2 -g .0078125 -b 1'); svmtrain(train_lab_mat(:,7), train_inst, '-c 2 -g .0078125 -b 1'); svmtrain(train_lab_mat(:,8), train_inst, '-c 2 -g .0078125 -b 1')];

	#predict training data with model. This should be very close to 100% accurate.
	printf("predicting training data\n")
	[predict_label_1, acc_1, prob_1] = svmpredict(train_lab_mat(:,1), train_inst, model_mat(1,:), '-b 1');
	[predict_label_2, acc_2, prob_2] = svmpredict(train_lab_mat(:,2), train_inst, model_mat(2,:), '-b 1');
	[predict_label_3, acc_3, prob_3] = svmpredict(train_lab_mat(:,3), train_inst, model_mat(3,:), '-b 1');
	[predict_label_4, acc_4, prob_4] = svmpredict(train_lab_mat(:,4), train_inst, model_mat(4,:), '-b 1');
	[predict_label_5, acc_5, prob_5] = svmpredict(train_lab_mat(:,5), train_inst, model_mat(5,:), '-b 1');
	[predict_label_6, acc_6, prob_6] = svmpredict(train_lab_mat(:,6), train_inst, model_mat(6,:), '-b 1');
	[predict_label_7, acc_7, prob_7] = svmpredict(train_lab_mat(:,7), train_inst, model_mat(7,:), '-b 1');
	[predict_label_8, acc_8, prob_8] = svmpredict(train_lab_mat(:,8), train_inst, model_mat(8,:), '-b 1');

	#predict cross-validation data with model. This should be as accurate as possible.
	printf("predicting cross-validation\n")
	[predict_label_1, acc_1, prob_1] = svmpredict(cross_lab_mat(:,1), cross_inst, model_mat(1,:), '-b 1');
	[predict_label_2, acc_2, prob_2] = svmpredict(cross_lab_mat(:,2), cross_inst, model_mat(2,:), '-b 1');
	[predict_label_3, acc_3, prob_3] = svmpredict(cross_lab_mat(:,3), cross_inst, model_mat(3,:), '-b 1');
	[predict_label_4, acc_4, prob_4] = svmpredict(cross_lab_mat(:,4), cross_inst, model_mat(4,:), '-b 1');
	[predict_label_5, acc_5, prob_5] = svmpredict(cross_lab_mat(:,5), cross_inst, model_mat(5,:), '-b 1');
	[predict_label_6, acc_6, prob_6] = svmpredict(cross_lab_mat(:,6), cross_inst, model_mat(6,:), '-b 1');
	[predict_label_7, acc_7, prob_7] = svmpredict(cross_lab_mat(:,7), cross_inst, model_mat(7,:), '-b 1');
	[predict_label_8, acc_8, prob_8] = svmpredict(cross_lab_mat(:,8), cross_inst, model_mat(8,:), '-b 1');

	#predict test data with model. Note that test labels are just placeholders
	#to actually analyze predictions you must look at individual probabilities
	printf("predicting test set\n")
	[predict_label_1, acc_1, prob_1] = svmpredict(test_lab_mat(:,1), test_inst, model_mat(1,:), '-b 1');
	[predict_label_2, acc_2, prob_2] = svmpredict(test_lab_mat(:,2), test_inst, model_mat(2,:), '-b 1');
	[predict_label_3, acc_3, prob_3] = svmpredict(test_lab_mat(:,3), test_inst, model_mat(3,:), '-b 1');
	[predict_label_4, acc_4, prob_4] = svmpredict(test_lab_mat(:,4), test_inst, model_mat(4,:), '-b 1');
	[predict_label_5, acc_5, prob_5] = svmpredict(test_lab_mat(:,5), test_inst, model_mat(5,:), '-b 1');
	[predict_label_6, acc_6, prob_6] = svmpredict(test_lab_mat(:,6), test_inst, model_mat(6,:), '-b 1');
	[predict_label_7, acc_7, prob_7] = svmpredict(test_lab_mat(:,7), test_inst, model_mat(7,:), '-b 1');
	[predict_label_8, acc_8, prob_8] = svmpredict(test_lab_mat(:,8), test_inst, model_mat(8,:), '-b 1');

	#print out individual probabilities for each test case
	#note that the for probability and the against probability may be switched
	#but it is usually pretty easy to see which is which
	printf("test 1\n")
	printf("%f\t%f\n", prob_1(1,1),prob_1(1,2))
	printf("%f\t%f\n", prob_2(1,1),prob_2(1,2))
	printf("%f\t%f\n", prob_3(1,1),prob_3(1,2))
	printf("%f\t%f\n", prob_4(1,1),prob_4(1,2))
	printf("%f\t%f\n", prob_5(1,1),prob_5(1,2))
	printf("%f\t%f\n", prob_6(1,1),prob_6(1,2))
	printf("%f\t%f\n", prob_7(1,1),prob_7(1,2))
	printf("%f\t%f\n\n", prob_8(1,1),prob_8(1,2))

	printf("test 2\n")
	printf("%f\t%f\n", prob_1(2,1),prob_1(2,2))
	printf("%f\t%f\n", prob_2(2,1),prob_2(2,2))
	printf("%f\t%f\n", prob_3(2,1),prob_3(2,2))
	printf("%f\t%f\n", prob_4(2,1),prob_4(2,2))
	printf("%f\t%f\n", prob_5(2,1),prob_5(2,2))
	printf("%f\t%f\n", prob_6(2,1),prob_6(2,2))
	printf("%f\t%f\n", prob_7(2,1),prob_7(2,2))
	printf("%f\t%f\n\n", prob_8(2,1),prob_8(2,2))

	printf("test 3\n")
	printf("%f\t%f\n", prob_1(3,1),prob_1(3,2))
	printf("%f\t%f\n", prob_2(3,1),prob_2(3,2))
	printf("%f\t%f\n", prob_3(3,1),prob_3(3,2))
	printf("%f\t%f\n", prob_4(3,1),prob_4(3,2))
	printf("%f\t%f\n", prob_5(3,1),prob_5(3,2))
	printf("%f\t%f\n", prob_6(3,1),prob_6(3,2))
	printf("%f\t%f\n", prob_7(3,1),prob_7(3,2))
	printf("%f\t%f\n\n", prob_8(3,1),prob_8(3,2))

	printf("test 4\n")
	printf("%f\t%f\n", prob_1(4,1),prob_1(4,2))
	printf("%f\t%f\n", prob_2(4,1),prob_2(4,2))
	printf("%f\t%f\n", prob_3(4,1),prob_3(4,2))
	printf("%f\t%f\n", prob_4(4,1),prob_4(4,2))
	printf("%f\t%f\n", prob_5(4,1),prob_5(4,2))
	printf("%f\t%f\n", prob_6(4,1),prob_6(4,2))
	printf("%f\t%f\n", prob_7(4,1),prob_7(4,2))
	printf("%f\t%f\n\n", prob_8(4,1),prob_8(4,2))

	printf("test 5\n")
	printf("%f\t%f\n", prob_1(5,1),prob_1(5,2))
	printf("%f\t%f\n", prob_2(5,1),prob_2(5,2))
	printf("%f\t%f\n", prob_3(5,1),prob_3(5,2))
	printf("%f\t%f\n", prob_4(5,1),prob_4(5,2))
	printf("%f\t%f\n", prob_5(5,1),prob_5(5,2))
	printf("%f\t%f\n", prob_6(5,1),prob_6(5,2))
	printf("%f\t%f\n", prob_7(5,1),prob_7(5,2))
	printf("%f\t%f\n\n", prob_8(5,1),prob_8(5,2))

	printf("test 6\n")
	printf("%f\t%f\n", prob_1(6,1),prob_1(6,2))
	printf("%f\t%f\n", prob_2(6,1),prob_2(6,2))
	printf("%f\t%f\n", prob_3(6,1),prob_3(6,2))
	printf("%f\t%f\n", prob_4(6,1),prob_4(6,2))
	printf("%f\t%f\n", prob_5(6,1),prob_5(6,2))
	printf("%f\t%f\n", prob_6(6,1),prob_6(6,2))
	printf("%f\t%f\n", prob_7(6,1),prob_7(6,2))
	printf("%f\t%f\n\n", prob_8(6,1),prob_8(6,2))

	printf("test 7\n")
	printf("%f\t%f\n", prob_1(7,1),prob_1(7,2))
	printf("%f\t%f\n", prob_2(7,1),prob_2(7,2))
	printf("%f\t%f\n", prob_3(7,1),prob_3(7,2))
	printf("%f\t%f\n", prob_4(7,1),prob_4(7,2))
	printf("%f\t%f\n", prob_5(7,1),prob_5(7,2))
	printf("%f\t%f\n", prob_6(7,1),prob_6(7,2))
	printf("%f\t%f\n", prob_7(7,1),prob_7(7,2))
	printf("%f\t%f\n\n", prob_8(7,1),prob_8(7,2))

endfunction

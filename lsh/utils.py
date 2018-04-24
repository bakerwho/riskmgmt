from lsh import *

def get_largest_key_val(data_dict):
	k = max(data_dict.keys())
	return k, data_dict[k]


def is_number(s):
	try:
		float(s)
		return True
	except:
		return False

def add_row_to_DF(df, row):
	assert isinstance(df, pd.DataFrame)
	cols = df.columns
	assert len(row) == len(cols)
	if isinstance(row, list):
		df = df.append({cols[i] : row[i] for i in range(len(cols))}, ignore_index=True)
	elif isinstance(row, dict):
		assert set(row.keys()) == set(cols)
		df = df.append({k : row[k] for k in cols})
	else:
		raise ValueError('Invalid row')	
	return df
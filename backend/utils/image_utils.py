def crop_item(image,bbox):

    x1,y1,x2,y2 = bbox

    return image[y1:y2, x1:x2]